$().ready(function() {
    $("#register").validate({
        rules: {
            username: {
                required: true,
                minlength: 6
            },
            pwd: {
                required: true,
                minlength: 8
            },
            pwd2: {
                required: true,
                equalTo: "#pwd"
            },
            email: {
                required: true,
                email: true
            }
        },
        messages: {
            username: {
                required: "Please enter an username",
                minlength: "Username is too short"
            },
            pwd: {
                required: "Please provide a password",
                minlength: "Password is too short"
            },
            pwd2: {
                required: "Please retype password",
                equalTo: "Passwords must match"
            },
            email: {
                required: "Please provide an email address",
                email: "Please provide a valid email address"
            }
        }
    });
});
