function getFeedback() {
    let utorID = $("#instructor-options option:selected").attr("name");
    let feedback = $("#feedback-text").val();
    $.post("/feedback", {
        instructor_id: utorID,
        feedback: feedback
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