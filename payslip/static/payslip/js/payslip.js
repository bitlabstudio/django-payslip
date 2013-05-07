$(document).ready(function() {
    $('#payslipMenu .printButton').click(function() {
        $('#payslipMenu').remove();
        window.print();
        return false;
    });
});