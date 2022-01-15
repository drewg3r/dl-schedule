function getCurrentEvent() {
    const url = "/api/event/now?api_token=" + getApiToken();

    let xhr = new XMLHttpRequest();
    xhr.open("GET", url);

    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            const currentEvent = JSON.parse(xhr.responseText);
            if (currentEvent["event"]) {
                document.getElementById("currentEventAbbr").innerHTML =
                    currentEvent["event"]["subject"]["abbr"] +
                    "<span class='ms-1 text-muted fs-6'>" +
                    currentEvent["event"]["start_time_str"] + "-" + currentEvent["event"]["end_time_str"] +
                    "</span>";

                document.getElementById("currentEventName").innerHTML = currentEvent["event"]["subject"]["name"];
                document.getElementById("currentEventLecturer").innerHTML = "Lecturer: " + currentEvent["event"]["subject"]["lecturer"];
                document.getElementById("currentEventLink").setAttribute("href", currentEvent["event"]["subject"]["link"]);
                document.getElementById("currentEventLink").innerHTML = "Lesson link";
                document.getElementById("currentEventTimeLeft").innerHTML = "Time left: " + currentEvent["time_left_min"] + "min";
            } else {
                document.getElementById("currentEventAbbr").innerHTML = "Free time"
                document.getElementById("currentEventName").innerHTML = "";
                document.getElementById("currentEventLecturer").innerHTML = "";
                document.getElementById("currentEventLink").innerHTML = "";
                document.getElementById("currentEventTimeLeft").innerHTML = "";
            }
        }};

    xhr.send(null);
}

function getNextEvent() {
    const url = "/api/event/next?api_token=" + getApiToken();

    let xhr = new XMLHttpRequest();
    xhr.open("GET", url);

    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            const nextEvent = JSON.parse(xhr.responseText);
            if (nextEvent["event"]) {
                document.getElementById("nextEventAbbr").innerHTML =
                    nextEvent["event"]["subject"]["abbr"] +
                    "<span class='ms-1 text-muted fs-6'>" +
                    nextEvent["event"]["start_time_str"] + "-" + nextEvent["event"]["end_time_str"] +
                    "</span>";

                document.getElementById("nextEventName").innerHTML = nextEvent["event"]["subject"]["name"];
                document.getElementById("nextEventLecturer").innerHTML = "Lecturer: " + nextEvent["event"]["subject"]["lecturer"];
                document.getElementById("nextEventLink").setAttribute("href", nextEvent["event"]["subject"]["link"]);
                document.getElementById("nextEventLink").innerHTML = "Lesson link";
            } else {
                document.getElementById("nextEventAbbr").innerHTML = "That's all for today"
                document.getElementById("nextEventName").innerHTML = "";
                document.getElementById("nextEventLecturer").innerHTML = "";
                document.getElementById("nextEventLink").innerHTML = "";
            }
        }};

    xhr.send(null);
}
