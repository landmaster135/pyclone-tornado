var id_list = ['#warmscore', '#freq_inweek']

// Show value of range (input type="range": warmscore id in addcloth.html and editcloth.html)
$('#warmscore').on("input", function() {
    $('.output_w').val(this.value);
}).trigger("change");
// Show value of range (input type="range": freq_inweek id in addcloth.html and editcloth.html)
$('#freq_inweek').on("input", function() {
    $('.output_f').val(this.value);
}).trigger("change");
// Show value of range (input type="range": comfort id in index.html)
$('#comfort').on("input", function() {
    $('.output_c').val(this.value);
}).trigger("change");
// Change appearance of file (input type="file" in addcloth.html and editcloth.html)
$(function(){
    $("input[type='file']").on('change',function(){
        var file = $(this).prop('files')[0];
        $(".filename").remove();
        if (file != undefined) { // ファイルがあるなら、
            $("#file-group").append('<span class="filename"></span>');
            $("#file-label").addClass('changed');
            $(".filename").html(file.name);
        }else{
            $("#file-label").removeClass('changed');
        }
    });
});
// Stop submitting in the case of exception (form tag in addcloth.html and editcloth.html)
$(function($){
    $('#button-submit').click(function (event){
        // $("#form-alert").remove(); // 下のappendとセット。
        event.preventDefault(); // ボタンのイベントをキャンセルする。
        $.ajax({
            type: 'POST',
            url : '../checkcloth',
            data: $(this).parent('form').serialize(),
            dataType: 'json',
            // contentType: 'application/json' // サーバに送信するデータのtype
            // success: function (data, dataType) { //非同期で通信成功時に読み出される [200 OK 時]
            // }
            // error: function (XMLHttpRequest, textStatus, errorThrown) {
            // }
            // complete: function(XMLHttpRequest, textStatus) {
            // }
        }).done(function (data) { //非同期で通信成功時に読み出される [200 OK 時]
            console.log("せいこう");
            // console.log(data.ResultSet.message);
            document.clothform.submit(); // submit送信
        }).fail(function (err) { //非同期で通信失敗時に読み出される [400 NG 時]
            console.log("しっぱい");
            // $("#form-alert").append('<span class="alert"></span>'); // 出来なかった。
            $(".alert").html("Anywhere is empty or wardrobe-name is unfortunate.");
        }).always(function () { //通信状態に関係なく毎回読み出される
            console.log("いつもどおり");
        })
    });
});
