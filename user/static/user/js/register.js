$(function () {
    $(".role-selector").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var text = self.text();
        var roleE = $("input[name=role_name]");
        roleE.attr('value', text)
    });
    $(".gender-selector").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var text = self.text();
        var genderE = $("input[name=gender_name]");
        genderE.attr('value', text)
    });
    $(".question-selector").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var text = self.text();
        var questionE = $("input[name=question_text]");
        questionE.attr('value', text)
    })
});