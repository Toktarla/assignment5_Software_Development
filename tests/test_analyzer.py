import pytest

from sentiment_app.analyzer import analyze_comment


def test_negative_transfer_tax():
    result = analyze_comment("Аударым салығы халыққа ауыр тиіп тұр.")
    assert result.label == "negative"
    assert result.topic == "mobile_transfer_tax"


def test_positive_egov():
    result = analyze_comment("eGov Mobile-дан құжат алу ыңғайлы болды.")
    assert result.label == "positive"
    assert result.topic == "egov_identity"


def test_negation_is_not_praise():
    result = analyze_comment("Бұл шешім дұрыс емес.")
    assert result.label == "negative"


def test_neutral_when_there_is_no_cue():
    result = analyze_comment("Заңның әсері әлі белгісіз.")
    assert result.label == "neutral"
    assert result.topic == "general_policy"


def test_school_and_pension():
    school = analyze_comment("Жаңа мектепке ризамын.")
    pension = analyze_comment("Зейнетақы туралы шешімді күтеміз.")
    assert school.label == "positive"
    assert school.topic == "school_construction"
    assert pension.label == "neutral"
    assert pension.topic == "pension_indexation"


def test_blank_text_is_rejected():
    with pytest.raises(ValueError):
        analyze_comment("   ")
