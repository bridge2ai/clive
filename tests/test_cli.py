"""Tests for the CLI."""

import unittest

from click.testing import CliRunner

from clive.cli import main

class TestCommandLineInterface(unittest.TestCase):
    """Tests all command-line subcommands."""

    def setUp(self) -> None:
        runner = CliRunner(mix_stderr=False)
        self.runner = runner
    
    def test_main_help(self):
        result = self.runner.invoke(main, ["--help"])
        out = result.stdout
        self.assertEqual(0, result.exit_code)
