function submit() {
    var left_is_ours = imageMetadata["left_is_ours"];
    var left = $( "#left" ).hasClass("highlight");
    var right = $( "#right" ).hasClass("highlight");
    var annotation = null;
    if (left && right) {
        annotation = 1;
    } else if (left) {
        if (left_is_ours) {
            annotation = 2;
        } else {
            annotation = 0;
        }
    } else if (right) {
        if (left_is_ours) {
            annotation = 0;
        } else {
            annotation = 2;
        }
    } else {
        annotation = -1
    }
    imageMetadata["annotation"] = annotation;
    console.log(imageMetadata);
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "/submit",
        data: JSON.stringify(imageMetadata),
        success: function (data) {
            console.log(imageMetadata);
        },
        fail: function (data) {
            alert("POST failed");
        },
        dataType: "json",
    });
}


function selectLeft(){
    if ($( "#right" ).hasClass("highlight")) {
        $("#right").removeClass("highlight");
    }
    if (!$( "#left" ).hasClass("highlight")) {
        $("#left").addClass("highlight");
    }
}

function selectRight() {
    if ($( "#left" ).hasClass("highlight")) {
        $("#left").removeClass("highlight");
    }
    if (!$( "#right" ).hasClass("highlight")) {
        $("#right").addClass("highlight");
    }
}


function selectBoth() {
    if (!$( "#left" ).hasClass("highlight")) {
        $("#left").addClass("highlight");
    }
    if (!$( "#right" ).hasClass("highlight")) {
        $("#right").addClass("highlight");
    }
}


function clearSelection() {
    if ($( "#left" ).hasClass("highlight")) {
        $("#left").removeClass("highlight");
    }
    if ($( "#right" ).hasClass("highlight")) {
        $("#right").removeClass("highlight");
    }
}


function nextImage() {
    index = parseInt(imageMetadata["index"]);
    if (index >= 49) {
        return;
    }
    var currentURL = window.location.href
    var segments = currentURL.split("/")
    segments[segments.length - 1] = String(index + 1);
    var newURL = segments.join("/");
    window.location.href = newURL;
    console.log(newURL);
}

function prevImage() {
    index = parseInt(imageMetadata["index"]);
    if (index <= 0) {
        return;
    }
    var currentURL = window.location.href
    var segments = currentURL.split("/")
    segments[segments.length - 1] = String(index - 1);
    console.log(segments);
    var newURL = segments.join("/");
    window.location.href = newURL;
    console.log(newURL);
}

$(document).keydown(function(event){
    if (event.key == 'w') {
        selectLeft();
    } else if (event.key == 'e') {
        selectBoth();
    } else if (event.key == 'r') {
        selectRight()
    } else if (event.key == "ArrowLeft") {
        submit();
        prevImage();
    } else if (event.key == "ArrowRight") {
        submit();
        nextImage();
    } else if (event.key == " ") {
        clearSelection();
    } else if (event.key == "Enter") {
        submit();
        location.reload();
    }
});