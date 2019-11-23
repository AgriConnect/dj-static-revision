import os
import shutil
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tests.django_settings')  # NOQA

import django
django.setup()   # NOQA

from dulwich.repo import Repo
from dulwich.errors import NotGitRepository
from dj_static_revision.utils import get_source_revision


TEST_DATA = 'aabbcc'


class TestGetSourceRevision:
    def setup(self):
        self.original_revision = None

    def test_normal_from_file(self):
        folder = Path.cwd()
        filepath = folder / '.version'
        filepath.write_text(TEST_DATA)
        revision = get_source_revision()
        assert revision == TEST_DATA

    def test_normal_from_repo(self):
        # Create repo
        folder = Path.cwd()
        try:
            rp = Repo(str(folder))
        except NotGitRepository:
            rp = Repo.init(str(folder))
        try:
            version = rp.head().decode()
            self.original_revision = version
        except KeyError:
            FILE_NAME_TEST = 'file_test.txt'
            test_file = folder / FILE_NAME_TEST
            test_file.touch()
            rp.stage(FILE_NAME_TEST.encode())
            version = rp.do_commit(b'Test commit').decode()
        v = get_source_revision()
        assert v == version[:10]

    def teardown(self):
        folder = Path.cwd()
        try:
            (folder / '.version').unlink()
        except FileNotFoundError:
            pass
        if self.original_revision is None:
            # Remove the Git repo created in test
            try:
                rp = Repo(str(folder))
                head = rp[rp.head()]
                if not len(head.parents):
                    shutil.rmtree(folder / '.git')
            except NotGitRepository:
                pass
