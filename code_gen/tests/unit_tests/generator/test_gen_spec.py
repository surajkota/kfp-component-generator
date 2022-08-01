from code_gen.generator.gen_spec import (
    get_spec_input_snippets,
    get_spec_output_snippets,
)
from test_variables import (
    input_spec_all,
    input_spec_required,
    output_statuses,
    crd_name,
)


def test_get_spec_input_snippets():
    """Test get_spec_input_snippets()."""

    (
        _spec_inputs_defi_snippet,
        _spec_inputs_validators_snippet,
    ) = get_spec_input_snippets(input_spec_all, input_spec_required)
    assert (
        _spec_inputs_defi_snippet
        == """
    name: Input
    description: Input
    type: string
    required: true
    """
    )
    assert (
        _spec_inputs_validators_snippet
        == """
    name=InputValidator(
        input_type=string,
        description="Input",
        required=True
    ), """
    )


if __name__ == "__main__":
    (
        _spec_inputs_defi_snippet,
        _spec_inputs_validators_snippet,
    ) = get_spec_input_snippets(input_spec_all, input_spec_required)
    print(_spec_inputs_defi_snippet)
