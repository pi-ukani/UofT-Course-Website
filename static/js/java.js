function getFeedback() {
    let utorID = $("#instructor-options option:selected").attr("name");
    let feedback = $("#feedback-text").val();
    $.post("/feedback", {
        instructor_id: utorID,
        feedback: feedback
    });
}

function updateMarks() {
    master_marks = {
        "remarks": []
    }
    $("#resp-table-body .resp-table-row").each(function () {
        utorid = $(this).attr("name");
        marks = $(this).find(".mark-input");
        if (typeof utorid !== 'undefined') {
            student = {
                "utorid": utorid
            }
            curr_stu_marks = {}
            marks.each(function () {
                assignment_name = ($(this).attr("name"));
                assignment_mark = ($(this).val());
                curr_stu_marks[assignment_name] = assignment_mark
            });
            student["marks"] = curr_stu_marks
            master_marks["remarks"].push(student)
        }
    });

    $.ajax({
        url: "/remark",
        type: "POST",
        data: JSON.stringify(master_marks),
        contentType: "application/json",
    });

}