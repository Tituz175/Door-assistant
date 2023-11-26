$(document).ready(function () {
  // Handle form submission
  $("form").on("submit", function (e) {
    e.preventDefault();

    // Get the value from the input field
    const number = $("form input").val();

    // Disable input, hide button, and show stop button
    $("form input").prop("disabled", true);
    $("form button").addClass("hidden");
    $("div #stop_camera").removeClass("hidden");

    // Reset the form
    $(this)[0].reset();

    // Make an AJAX request to start the camera
    $.ajax({
      url: "http://127.0.0.1:5000/start_camera",
      method: "GET",
      success: function (res) {
        console.log(res);
      },
    });
  });

  // Handle stop button click
  $("div #stop_camera").on("click", function (e) {
    // Enable input, show button, and hide stop button
    $("form input").prop("disabled", false);
    $("form button").removeClass("hidden");
    $("div #stop_camera").addClass("hidden");

    // Make an AJAX request to stop the camera
    $.ajax({
      url: "http://127.0.0.1:5000/stop_camera",
      method: "GET",
      success: function (res) {
        console.log(res);
      },
    });
  });
});
