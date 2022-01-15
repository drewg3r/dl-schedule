function getEvent(eventId) {
    const url = "/api/event?api_token=" + getApiToken() + "&event_id=" + eventId;

    let xhr = new XMLHttpRequest();
    xhr.open("GET", url);

    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            const event =  JSON.parse(xhr.responseText)["event"];
            if (event) {
                const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
                document.getElementById("inputEventStartView").value = event["start_time_str"];
                document.getElementById("inputEventEndView").value = event["end_time_str"];
                console.log(event);
                document.getElementById("inputEventWeekdayView").value = weekdays[event["weekday"]];

                const subject = event["subject"];
                document.getElementById("inputSubjectNameView").value = subject["name"];
                document.getElementById("inputSubjectNameEdit").value = subject["name"];

                document.getElementById("inputSubjectAbbrView").value = subject["abbr"];
                document.getElementById("inputSubjectAbbrEdit").value = subject["abbr"];

                document.getElementById("inputSubjectLecturerView").value = subject["lecturer"];
                document.getElementById("inputSubjectLecturerEdit").value = subject["lecturer"];

                document.getElementById("inputSubjectLinkView").value = subject["link"];
                document.getElementById("inputSubjectLinkEdit").value = subject["link"];

                document.getElementById("editSubjectCancelButton").setAttribute("data-event-id", eventId);
                document.getElementById("editSubjectCancelButton").setAttribute("data-subject-id", subject["id"]);
                document.getElementById("editSubjectSaveButton").onclick=function(){putSubject(true)};
            } else {
                console.log(xhr.responseText);
            }
        }};

    xhr.send(null);
}

function deleteEvent(eventId) {
    const url = "/api/event";

    let xhr = new XMLHttpRequest();
    xhr.open("DELETE", url);

    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    const body = 'event_id=' + eventId +
        '&api_token=' + getApiToken();

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            location.reload();
        }};

    xhr.send(body);
}

function createEvent(startTime, endTime, weekday, subjectId) {
    const url = "/api/event";

    let xhr = new XMLHttpRequest();
    xhr.open("POST", url);

    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    const body = 'start_time=' + startTime +
        '&end_time=' + endTime +
        '&weekday=' + weekday +
        '&subject_id=' + subjectId +
        '&api_token=' + getApiToken();

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            location.reload();
        }};


    xhr.send(body);
}

function modalAddEventSubmit() {
    const timeStartH = document.getElementById("inputTimeStartH").value;
    const timeStartM = document.getElementById("inputTimeStartM").value;
    const timeEndH = document.getElementById("inputTimeEndH").value;
    const timeEndM = document.getElementById("inputTimeEndM").value;

    createEvent(
        parseInt(timeStartH)*60+parseInt(timeStartM),
        parseInt(timeEndH)*60+parseInt(timeEndM),
        document.getElementById("weekday").value,
        document.getElementById("subjectSelect").value,
    )

    document.getElementById("inputTimeStartH").value = "";
    document.getElementById("inputTimeStartM").value = "";
    document.getElementById("inputTimeEndH").value = "";
    document.getElementById("inputTimeEndM").value = "";
    document.getElementById("subjectSelect").value = "";
}
