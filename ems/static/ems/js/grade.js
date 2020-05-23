$(function () {
    $('.btn-submit').click(function (event) {
        event.preventDefault();
        var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        var pointInputs = $("input[name=point]");
        var points = [];
        var url = '/ems/grade/1';
        pointInputs.each(function () {
            self = $(this);
            var grade_id = self.attr('data-id');
            var point = self.val();
            if(point>100){alert('注意，大于100的分数将不会生效！')}
            else if(point<0){alert('注意，小于0的分数将不会生效！！')}
            else {points.push({
                'grade_id': grade_id,
                'point': point,
            });}
        });
        console.log(points);
        $.ajax({
            'method': 'post',
            'url': url,
            'dataType': 'JSON',
            'data': {
                'points': JSON.stringify(points),
                'csrfmiddlewaretoken': csrf_token,
            },
            'success': function (response) {
                    var msg = response['message'];
                    alert(msg);
                    window.location.reload()
                },
            'fail': function () {
                alert('提交失败，请稍后重试或联系管理员！');
            }
        })

    })
});

//成绩操作