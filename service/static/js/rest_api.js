Context = {}


$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#rec_rec_id").val(res.rec_id);
        $("#rec_recommendation_name").val(res.recommendation_name);
        $("#rec_source_pid").val(res.source_pid);
        $("#rec_name").val(res.name);
        $("#rec_type").val(res.type);
        $("#rec_number_of_likes").val(res.number_of_likes);
        $("#rec_number_of_dislikes").val(res.number_of_dislikes);
    }

    /// Clears all form fields
    function clear_form_data() {
        // $("#rec_rec_id").val("");
        $("#rec_recommendation_name").val("");
        $("#rec_source_pid").val("");
        $("#rec_name").val("");
        $("#rec_type").val("");
        $("#rec_number_of_likes").val("");
        $("#rec_number_of_dislikes").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Recommendation
    // ****************************************

    $("#create-btn").click(function () {

        // let rec_id = $("#rec_rec_id").val();
        let recommendation_name = $("#rec_recommendation_name").val();
        let source_pid = $("#rec_source_pid").val();
        let name = $("#rec_name").val();
        let type = $("#rec_type").val();
        let number_of_likes = $("#rec_number_of_likes").val();
        let number_of_dislikes = $("#rec_number_of_dislikes").val();

        let data = {
            // "rec_id": rec_id,
            "recommendation_name": recommendation_name,
            "source_pid": source_pid,
            "name": name,
            "type": type,
            "number_of_likes": number_of_likes,
            "number_of_dislikes": number_of_dislikes
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/api/recommendations",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Recommendation
    // ****************************************

    $("#update-btn").click(function () {

        let rec_id = $("#rec_rec_id").val();
        let recommendation_name = $("#rec_recommendation_name").val();
        let source_pid = $("#rec_source_pid").val();
        let name = $("#rec_name").val();
        let type = $("#rec_type").val();
        let number_of_likes = $("#rec_number_of_likes").val();
        let number_of_dislikes = $("#rec_number_of_dislikes").val();

        let data = {
            // "rec_id": rec_id,
            "recommendation_name": recommendation_name,
            "source_pid": source_pid,
            "name": name,
            "type": type,
            "number_of_likes": number_of_likes,
            "number_of_dislikes": number_of_dislikes
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/api/recommendations/${rec_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Recommendation
    // ****************************************

    $("#retrieve-btn").click(function () {

        let rec_id = $("#rec_rec_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/recommendations/${rec_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Recommendation
    // ****************************************

    $("#delete-btn").click(function () {

        let rec_id = $("#rec_rec_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/recommendations/${rec_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Recommendation has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#rec_rec_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Recommendation
    // ****************************************

    $("#search-btn").click(function () {


        let recommendation_name = $("#rec_recommendation_name").val();
        let source_pid = $("#rec_source_pid").val();
        let name = $("#rec_name").val();
        let type = $("#rec_type").val();

        let queryString = ""

        if (recommendation_name) {
            queryString += 'recommendation_name=' + recommendation_name
        }

        if (source_pid) {
            queryString += 'source_pid=' + source_pid
        }

        if (name) {
            queryString += 'name=' + name
        }

        if (type) {
            if (queryString.length > 0) {
                queryString += '&type=' + type
            } else {
                queryString += 'type=' + type
            }
        }

        $("#flash_message").empty();

        Context.queryString = queryString

        let ajax = $.ajax({
            type: "GET",
            url: `/api/recommendations?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(listResult);

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });


    function refreshOnCurrentContext(){
        const queryString = Context.queryString
        let ajax = $.ajax({
            type: "GET",
            url: `/api/recommendations?${queryString}`,
            contentType: "application/json",
            data: ''
        })
    
        ajax.done(listResult);
    
        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    }
    
    function listResult(res){
        flash_message("Success")

        $("#search_results").empty();
        let table = '<table class="table table-striped" cellpadding="10" id="content-table">'
        table += '<thead><tr>'
        table += '<th class="col-md-1">ID</th>'
        table += '<th class="col-md-1">Name</th>'
        table += '<th class="col-md-1">Source ID</th>'
        table += '<th class="col-md-1">Source Name</th>'
        table += '<th class="col-md-2">Type</th>'
        table += '<th class="col-md-1">like</th>'
        table += '<th class="col-md-1">dislike</th>'
        table += '<th class="col-md-2">like button</th>'
        table += '<th class="col-md-2">dislike button</th>'
        table += '</tr></thead><tbody>'
        let firstRec = "";
        for(let i = 0; i < res.length; i++) {
            let rec = res[i];
            //console.log(rec)
            //console.log(rec)
            table +=  `<tr id="row_${i}">
                <td>${rec.rec_id}</td>
                <td>${rec.recommendation_name}</td>
                <td>${rec.source_pid}</td>
                <td>${rec.name}</td>
                <td>${rec.type}</td>
                <td> <p id="like-${i}"> ${rec.number_of_likes} </p> </td>
                <td> <p id="dislike-${i}"> ${rec.number_of_dislikes} </p> </td>
                <td> <button id="like-button-${i}"> Like </button> </td>
                <td> <button id="dislike-button-${i}"> Dislike </button> </td>       
                </tr>
                `;
            if (i == 0) {
                firstRec = rec;
            }
        }            
        table += '</tbody></table>';    
        $("#search_results").append(table);
    
        $("#search_results").on("click", "button[id^='like-button-']", function() {
            // This function will be triggered when a like button is clicked
            const index = $(this).attr('id').split('-').pop();
            obj = res[index]
            update_like(obj)
        });
    
        $("#search_results").on("click", "button[id^='dislike-button-']", function() {
            // This function will be triggered when a dislike button is clicked
            let index = $(this).attr('id').split('-').pop();
            obj = res[index]
            update_dislike(obj)
        });
        
        // copy the first result to the form
        if (firstRec != "") {
            update_form_data(firstRec)
        }
          
    }
    
    function update_like(obj){
        const {rec_id,recommendation_name,source_pid, name, type, number_of_likes, number_of_dislikes} = obj
        let data = {
            "recommendation_name": recommendation_name,
            "source_pid": source_pid,
            "name": name,
            "type": type,
            "number_of_likes": number_of_likes+1,
            "number_of_dislikes": number_of_dislikes
        };
    
        $("#flash_message").empty();
    
        let ajax = $.ajax({
            type: "PUT",
            url: `/api/recommendations/${rec_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })
    
        ajax.done(function(res){
            flash_message("Success")
            refreshOnCurrentContext();
        });
    
        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    }
    
    function update_dislike(obj){
        const {rec_id,recommendation_name,source_pid, name, type, number_of_likes, number_of_dislikes} = obj
        let data = {
            "recommendation_name": recommendation_name,
            "source_pid": source_pid,
            "name": name,
            "type": type,
            "number_of_likes": number_of_likes,
            "number_of_dislikes": number_of_dislikes+1
        };
    
        $("#flash_message").empty();
    
        let ajax = $.ajax({
            type: "PUT",
            url: `/api/recommendations/${rec_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })
    
        ajax.done(function(res){
            flash_message("Success")
            refreshOnCurrentContext()
        });
    
        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    }


})