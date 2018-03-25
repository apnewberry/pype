
import pytest
from click.testing import CliRunner
from hypothesis import given
from hypothesis.strategies import text

import pype
import pype.app


@pytest.mark.parametrize(
    'args,  expected',
    [
        (['str.replace(?, ".", "!")', ('a.b.c',)], 'a!b!c\n'),
        (
            [
                '-icollections',
                '-ijson',
                'json.dumps(dict(collections.Counter(str.replace(?, ".", "!"))))',
                ('a.b.c',)
            ],
            '{"a": 1, "!": 2, "b": 1, "c": 1}'
        ),
        (
            [
                '-icollections',
                '-ijson',
                'str.replace(?, ".", "!") '
                '|| collections.Counter(?) '
                '|| dict(?) '
                '|| json.dumps(?) ',
                ('a.b.c',)
            ],
            '{"a": 1, "!": 2, "b": 1, "c": 1}'
        ),
        (
            [
                '-icollections',
                '-ijson',
                'str.replace(?, ".", "!") '
                '|| collections.Counter '
                '|| dict '
                '|| json.dumps ',
                ('a.b.c',)
            ],
            '{"a": 1, "!": 2, "b": 1, "c": 1}'
        ),

    ]
)
def test_cli(args, expected):

    runner = CliRunner()
    result = runner.invoke(pype.app.cli, args)
    assert not result.exception
    assert result.output.strip() == expected.strip()


@pytest.mark.parametrize(
    'command, expected',
    [
        ('str.upper(?)', str.upper),
        ('str.upper', str.upper),
    ]
)
@given(line=text())
def test_make_pipeline(command, line, expected):
    assert pype.app.make_pipeline(command)(line) == expected(line)
