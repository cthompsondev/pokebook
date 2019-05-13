

add_validations = function(){
    //EMAIL TAKEN VALIDATIONS
    $("#id_email").change(function () {
        var email = $(this).val();
        

        $.ajax({
        url: '/ajax/validate_email/',
        data: {
            'email': email
        },
        dataType: 'json',
        success: function (data) {
            if (data.is_taken) {
                $('#email_check').html('email taken')
                $("#regbutton").prop('disabled' , true)
            }
            else{
                $('#email_check').html('')
                form_validation(true)
            }
                
        }
        });

    });

    $(".pword").change(function() {
        
        pword = $("#password").val()
        pword2 = $("#confpassword").val()
        
        is_valid = pword == pword2
        if(pword.length < 8){
            $("#passwordlength_check").html('password must be atleast 8 characters')
            
        }
        else{
            $("#passwordlength_check").html('')
        }
        if(pword2.length < 8){
            $("#confpassword_check").html('confirmation password must be atleast 8 characters')
            
        }
        else{
            $("#confpassword_check").html('')
        }
        
        if(!is_valid){
            $("#password_check").html('password mismatch')
            $("#regbutton").prop('disabled' , true)
            form_validation()
            return
        }
        else{
            $("#password_check").html('')
            form_validation()
            return
        }
        
    })

    $("#first_name").change(function(){
        if($(this).val().length >= 2){
            $("#fname_check").html('')
            form_validation()
        }
        else{
            $("#fname_check").html('first name must be atleast 2 characters')
            $("#regbutton").prop('disabled' , true)
            form_validation()
        }
    })

    $("#last_name").change(function(){
        if($(this).val().length >= 2){
            $("#lname_check").html('')
            form_validation()
        }
        else{
            $("#lname_check").html('last name must be atleast 2 characters')
            $("#regbutton").prop('disabled' , true)
            form_validation()
        }
    })

    $("#birth_date_form").change(function(){
        bday = $("#birth_date")
        var d = new Date();
        var year = d.getFullYear();
        var month = d.getMonth();
        var day = d.getDate();
        var c = new Date(year - 13, month, day)
        var bdate = new Date(bday.val())
        if (bdate > c){
            $('#bday_check').html("You must be 13 years old to register")
            $("#regbutton").prop('disabled' , true)
            form_validation()
        }
        else{
            $('#bday_check').html("")
            form_validation()
        }


        
    })

    $("#alias").change(function(){
        if($(this).val().length >= 2){
            $("#alias_check").html('')
            form_validation()
        }
        else{
            $("#alias_check").html('alias must be atleast 2 characters')
            $("#regbutton").prop('disabled' , true)
            form_validation()
        }
    })


}

form_validation = function(fromemail = false){
    form = $("#reg_form")
    fname =$("#first_name")
    lname =$("#last_name")
    email =$("#id_email")
    password =$("#password")
    confpassword =$('#confpassword')
    alias =$("#alias")
    
    bday = $("#birth_date")
        var d = new Date();
        var year = d.getFullYear();
        var month = d.getMonth();
        var day = d.getDate();
        var c = new Date(year - 13, month, day)
        var bdate = new Date(bday.val())
    
    
    if( fname.val().length >=2 && lname.val().length >=2 &&password.val().length >= 8 &&confpassword.val().length >= 8 && password.val() == confpassword.val() &&alias.val().length >= 2 && bdate <= c){
        var re = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/;
        if(re.test(email.val().toUpperCase())){
            if(fromemail){
                $("#regbutton").prop('disabled' , false)
                $("#form_check").html('')
            }
            else{
                $("#id_email").change()
            }
        }


    }
    else{
        $("#form_check").html('Form errors exist or is incomplete')
        $("#regbutton").prop('disabled' , true)
    }

    
}