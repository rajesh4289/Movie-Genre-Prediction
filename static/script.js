function predictGenre() {
    var input = document.getElementById('fileInput');
    var file = input.files[0];

    var formData = new FormData();
    formData.append('file', file);

    $.ajax({
        type: 'POST',
        url: '/predict',
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            displayImage(file);
            displayPredictedGenres(response);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function displayImage(file) {
    var reader = new FileReader();
    reader.onload = function (e) {
        var imageDisplay = document.getElementById('imageDisplay');
        imageDisplay.innerHTML = '<img src="' + e.target.result + '" alt="Selected Image" />';
    };
    reader.readAsDataURL(file);
}


function displayPredictedGenres(response) {
    var predictedGenres = document.getElementById('predictedGenres');
    predictedGenres.innerHTML = 'Predicted Genres: ' + response;
}
