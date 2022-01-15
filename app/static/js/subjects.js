function getSubject(subjectId) {
    const url = "/api/subject?api_token=" + getApiToken() + "&id=" + subjectId;

    let xhr = new XMLHttpRequest();
    xhr.open("GET", url);

    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            const subject =  JSON.parse(xhr.responseText)["subject"];
            if (subject) {
                document.getElementById("inputSubjectNameView").value = subject["name"];
                document.getElementById("inputSubjectNameEdit").value = subject["name"];

                document.getElementById("inputSubjectAbbrView").value = subject["abbr"];
                document.getElementById("inputSubjectAbbrEdit").value = subject["abbr"];

                document.getElementById("inputSubjectLecturerView").value = subject["lecturer"];
                document.getElementById("inputSubjectLecturerEdit").value = subject["lecturer"];

                document.getElementById("inputSubjectLinkView").value = subject["link"];
                document.getElementById("inputSubjectLinkEdit").value = subject["link"];

                document.getElementById("editSubjectCancelButton").setAttribute("data-subject-id", subjectId);
            } else {
                console.log(xhr.responseText);
            }
        }};

    xhr.send(null);
}

function getSubjects(searchQuery) {
    let url;

    if (searchQuery){
        url = "/api/subjects/search?api_token=" + getApiToken() + "&name=" + searchQuery;
    } else {
        url = "/api/subjects?api_token=" + getApiToken();
    }

    let xhr = new XMLHttpRequest();
    xhr.open("GET", url);

    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            const subjects = JSON.parse(xhr.responseText)["subjects"];
            let table = "";
            for (let i = 0; i < subjects.length; i++) {
                table += "<tr>" +
                          "<td class='align-middle'>" + subjects[i]["name"] + "</td>" +
                          "<td class='text-end'>" +
                          "  <button type='button' class='btn btn-primary' data-subject-id='"+subjects[i]["id"]+"' data-bs-toggle='modal' data-bs-target='#viewSubjectModal'>Info</button>" +
                          "  <button type='button' class='btn btn-danger' data-subject-name='"+subjects[i]["name"]+"' data-subject-id='"+subjects[i]["id"]+"' data-bs-toggle='modal' data-bs-target='#removeSubjectModal'>Delete</button>" +
                          "</td>" +
                          "</tr>"
            }
            document.getElementById("subjectsTableBody").innerHTML = table;
        }};

    xhr.send(null);
}

function createSubject(name, abbr, lecturer, link) {
    const url = "/api/subject";

    let xhr = new XMLHttpRequest();
    xhr.open("POST", url);

    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    const body = 'name=' + encodeURIComponent(name) +
        '&abbr=' + encodeURIComponent(abbr) +
        '&lecturer=' + encodeURIComponent(lecturer) +
        '&link=' + encodeURIComponent(link) +
        '&api_token=' + getApiToken();

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            getSubjects();

            document.getElementById("inputSubjectName").value = "";
            document.getElementById("inputSubjectAbbr").value = "";
            document.getElementById("inputSubjectLecturer").value = "";
            document.getElementById("inputSubjectLink").value = "";
        }};

    xhr.send(body);
}

function putSubject(pageReload=false) {
    const id = document.getElementById("editSubjectCancelButton").getAttribute("data-subject-id");
    const name = document.getElementById("inputSubjectNameEdit").value;
    const abbr = document.getElementById("inputSubjectAbbrEdit").value;
    const lecturer = document.getElementById("inputSubjectLecturerEdit").value;
    const link = document.getElementById("inputSubjectLinkEdit").value;

    const url = "/api/subject";

    let xhr = new XMLHttpRequest();
    xhr.open("PUT", url);

    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    const body = 'name=' + encodeURIComponent(name) +
        '&abbr=' + encodeURIComponent(abbr) +
        '&lecturer=' + encodeURIComponent(lecturer) +
        '&link=' + encodeURIComponent(link) +
        '&id=' + encodeURIComponent(id) +
        '&api_token=' + getApiToken();

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (pageReload) {
                location.reload();
            } else {
                getSubjects();
            }
        }};

    xhr.send(body);
}

function deleteSubject(id) {
    if (id == null) {
        return;
    }

    const url = "/api/subject";

    let xhr = new XMLHttpRequest();
    xhr.open("DELETE", url);

    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    const body = 'id=' + encodeURIComponent(id) +
        '&api_token=' + encodeURIComponent(getApiToken());

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            getSubjects();
        }};


    xhr.send(body);
}

function modalAddSubjectSubmit() {
    createSubject(
        document.getElementById("inputSubjectName").value,
        document.getElementById("inputSubjectAbbr").value,
        document.getElementById("inputSubjectLecturer").value,
        document.getElementById("inputSubjectLink").value
    );

}