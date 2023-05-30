function submitUserInformation() {
    var sex = document.getElementById("sex").value;
    var age = document.getElementById("age").value;
    var score = document.getElementById("score").value;
    var smoke = document.getElementById("smoke").value;
    var stoke = document.getElementById("stoke").value;
    var diabetic = document.getElementById("diabetic").value;
    var kidney = document.getElementById("kidney").value;
    var bmi = document.getElementById("bmi").value;

    var url =
      "https://7ho5ohgnf7.execute-api.us-east-2.amazonaws.com/getPatient?sex=" +
      encodeURIComponent(sex) +
      "&age=" +
      encodeURIComponent(age) +
      "&score=" +
      encodeURIComponent(score) +
      "&smoke=" +
      encodeURIComponent(smoke) +
      "&stoke=" +
      encodeURIComponent(stoke) +
      "&diabetic=" +
      encodeURIComponent(diabetic) +
      "&kidney=" +
      encodeURIComponent(kidney) +
      "&bmi=" +
      encodeURIComponent(bmi);

    console.log("Hello, world!");
    console.log(url);
    $.ajax({
      url: url,
      type: "GET",
      success: function (result) {
        var params = new URLSearchParams(result);
        var predict = params.get("Prediction");
        var prob = params.get("Probability");
        var percentage = (prob * 100).toFixed(2) + "%";
        var result_pred;

        if (predict === "1") {
            result_pred = "Likely to have heart disease";
        } else if (predict === "0") {
            result_pred = "Unlikely to have heart disease";
        } else {
            result_pred = "error"; // optional fallback value if predict has a different value
        }

        console.log(result_pred); // Outputs either "yes" or "no"

        document.getElementById("apiResult").innerHTML =
          "Prediction Result: " +
          result_pred +
          "<br>Outcome Confidence: " +
          percentage +
          "<br>";

        const apiResultElement = document.getElementById("apiResult");

        // Get the API result value
        const apiResult = apiResultElement.textContent;

        if (result_pred.toLowerCase().includes("unlikely")) {
          apiResultElement.style.color = "#45a049";
          console.log("reach");
        } else {
          apiResultElement.style.color = "red";
        }
      },
      error: function (error) {
        console.log(error);
      },
    });
  }
