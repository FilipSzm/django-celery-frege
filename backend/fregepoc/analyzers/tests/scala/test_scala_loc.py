import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.tests.scala.constants import MOCKED_SCALA_FILES
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.factories import RepositoryFileFactory


@pytest.mark.django_db
class TestScalaAnalyzerLinesOfCode:
    @pytest.mark.parametrize(
        ["repo_file_params", "expected_loc"],
        [
            (
                {"repo_relative_file_path": "InsertionSort.scala"},
                23,
            ),
            (
                {"repo_relative_file_path": "EmptyFile.scala"},
                0,
            ),
            (
                {"repo_relative_file_path": "BinaryTree.scala"},
                44,
            ),
            (
                {"repo_relative_file_path": "PrimeNumbers.scala"},
                8,
            ),
        ],
    )
    def test_count_loc(
        self, repo_file_params, expected_loc, settings, dummy_repo
    ):
        settings.DOWNLOAD_PATH = MOCKED_SCALA_FILES
        analyzers = AnalyzerFactory.make_analyzers(
            ProgrammingLanguages.SCALA
        )
        repo_file = RepositoryFileFactory(
            repository=dummy_repo,
            language=ProgrammingLanguages.SCALA,
            **repo_file_params,
        )
        for analyzer in analyzers:
            actual = analyzer.analyze(repo_file)
            assert actual["lines_of_code"] == expected_loc
