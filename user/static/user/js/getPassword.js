$(function () {
    $(".question-selector").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var text = self.text();
        var questionE = $("input[name=question_text]");
        questionE.attr('value', text)
    })
});