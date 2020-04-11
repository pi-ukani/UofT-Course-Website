function myFunction() {
    var x = document.getElementById("main-nav-id");
    if (x.className === "main-nav") {
        x.className += " responsive";
    } else {
        x.className = "main-nav";
    }
}

function getFeedback() {
    let utorID = $("#instructor-options option:selected").attr("name");
    let feedback1 = $("#feedback-text1").val();
    let feedback2 = $("#feedback-text2").val();
    let feedback3 = $("#feedback-text3").val();
    let feedback4 = $("#feedback-text4").val();


    $.post("/feedback", {
        instructor_id: utorID,
        feedback1: feedback1,
        feedback2: feedback2,
        feedback3: feedback3,
        feedback4: feedback4,
    });
}

function updateMarks() {
    modified_grades = {
        "remarks": []
    }
    $("#row_group .ind_row").each(function () {
        utorid = $(this).attr("name");
        marks = $(this).find(".modify_grade");
        if (typeof utorid !== 'undefined') {
            student = {
                "username": utorid
            }
            current_grades = {}
            marks.each(function () {
                assignment_name = ($(this).attr("name"));
                assignment_mark = ($(this).val());
                current_grades[assignment_name] = assignment_mark
            });
            student["marks"] = current_grades
            modified_grades["remarks"].push(student)

        }

    });

    $.ajax({
        url: "/remark",
        type: "POST",
        data: JSON.stringify(modified_grades),
        contentType: "application/json",
        success: function () {
            location.reload();
            alert('Grades updated please refresh the page');
        }
    })
}
/* FOR HTML/CSS */
function myFunction() {
    var x = document.getElementById("main-nav-id");
    if (x.className === "main-nav") {
        x.className += " responsive";
    } else {
        x.className = "main-nav";
    }
}
//For assignments.html
function showA1Instructions() {
    document.getElementById('assn-1-instructions').style.display = "block";
    document.getElementById('assn-1-briefing').style.display = "none";
}

function showA2Instructions() {
    document.getElementById('assn-2-instructions').style.display = "block";
    document.getElementById('assn-2-briefing').style.display = "none";
}

function showA3Instructions() {
    document.getElementById('assn-3-instructions').style.display = "block";
    document.getElementById('assn-3-briefing').style.display = "none";
}

function showA1Briefing() {
    document.getElementById('assn-1-briefing').style.display = "block";
    document.getElementById('assn-1-instructions').style.display = "none";
}

function showA2Briefing() {
    document.getElementById('assn-2-briefing').style.display = "block";
    document.getElementById('assn-2-instructions').style.display = "none";
}

function showA3Briefing() {
    document.getElementById('assn-3-briefing').style.display = "block";
    document.getElementById('assn-3-instructions').style.display = "none";
}
