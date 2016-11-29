$(document).ready(function(){
    h = $(document).height();
    $('.parallax-window').height(h*0.17).css({'opacity': '0.9'});
});

function post_utf(txt) {
    var tosend = new Object();
    tosend.some = txt;
    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/toutf',
        dataType: 'json',
        data:  JSON.stringify({'utf': txt}),
        success: function(data) {
            $.each( data, function( key, val ) {
                console.log(val);
                $('#utf').val(val);
            });
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function post_sdx(txt) {
    var tosend = new Object();
    tosend.some = txt;
    rsp = [];
    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/toutf',
        dataType: 'json',
        data:  JSON.stringify({'sdx': txt}),
        success: function(data) {
            $.each( data, function( key, val ) {
                console.log(val);
                rsp.push(val);
            });
            $('#utf_sdx').val(rsp);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function post_final(txt) {
    $('#load').show();
    var tosend = new Object();
    tosend.some = txt;
    rsp = [];
    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/toutf',
        dataType: 'json',
        data:  JSON.stringify({'malformed': txt}),
        success: function(data) {
            $.each( data, function( key, val ) {
                console.log(val);
                rsp.push(val);
            });
            $('#incorrect_words').html('');
            for (i=0; i<rsp.length; i++) {
                $('#incorrect_words').append(' '+i + ':' + rsp[i] + '; ');
            }
            setTimeout(function(){
                post_features(txt);
            }, 3000);
        },
        error: function(error) {
            console.log(error);
        }
    });
}


function post_features(txt) {
    var tosend = new Object();
    tosend.some = txt;
    rsp = [];
    nms = [];
    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/toutf',
        dataType: 'json',
        data:  JSON.stringify({'features': txt}),
        success: function(data) {
            $.each( data, function( key, val ) {
                console.log(val);
                rsp.push(val);
                nms.push(key);
            });
            $('#features').html('');
            for (i=0; i<rsp.length; i++) {
                $('#features').append(' '+nms[i] + ':' + rsp[i] + '; ');
            }
            setTimeout(function(){
                select_features(txt);
            }, 3000);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function select_features(txt) {
    var tosend = new Object();
    tosend.some = txt;
    rsp = [];
    nms = [];
    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/toutf',
        dataType: 'json',
        data:  JSON.stringify({'self': txt}),
        success: function(data) {
            $.each( data, function( key, val ) {
                console.log(val);
                rsp.push(val);
                nms.push(key);
            });
            $('#features_sel').html('');
            for (i=0; i<rsp.length; i++) {
                $('#features_sel').append(' '+nms[i] + ':' + rsp[i] + '; ');
            }
            setTimeout(function(){
                ft_geo(rsp);
            }, 2000);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function ft_geo(txt) {
    var tosend = new Object();
    tosend.some = txt;
    rsp = [];
    nms = [];
    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/toutf',
        dataType: 'json',
        data:  JSON.stringify({'togeo': txt}),
        success: function(data) {
            $.each( data, function( key, val ) {
                console.log(val);
                rsp.push(val);
                nms.push(key);
            });
            $('#ft_ge').html('');
            for (i=0; i<rsp.length; i++) {
                $('#ft_ge').append(' '+nms[i] + ':' + rsp[i] + '; ');
            }
            setTimeout(function(){
                $('#load').hide();
            }, 500);
        },
        error: function(error) {
            console.log(error);
        }
    });
}




function intro() {
    t = 300;
    $('.hd_cont').each(function(i){
        if (i <= 3) {
            $(this).show('slide', {direction: 'left'}, t * (i+2)).css({'display': 'inline-block'});
            $('#img_' + i).show('slide', {direction: 'right'}, t * (i+3));
        }
        else{
            $(this).show('slide', {direction: 'right'}, t * (i+2)).css({'display': 'inline-block'});
            $('#img_' + i).show('slide', {direction: 'left'}, t * (i+3));
        }
    });
    setTimeout(function(){
        $('#svan').show('slow');
        $('#svan_l').show('slow');
    }, 4000);
}

function outline() {
    $('.outline').each(function(i){
        $(this).fadeIn(t * (i*7));
    });
}

function show_page(id) {
    $('#'+id).fadeIn(900);
}