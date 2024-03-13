function past_reports(){
    // document.body
	let past_record_box=`
	<div class="login-box">
		<h1>Check to past reports</h1>
		<form action="/past_records" method="POST">
			<label for="username">User ID:</label>
			<input type="text" id="username" name="username"><br><br>
			<label for="password">Password:</label>
			<input type="password" id="password" name="password"><br><br>
			<input type="submit" value="Login">
		</form>
	</div>
	`

	let add_report_box=`
	<div class="login-box">
		<h1>Check to add records</h1>
		<form action="/add_report_doctor_check" method="POST">
			<label for="username">User ID:</label>
			<input type="text" id="username" name="username"><br><br>
			<label for="password">Password:</label>
			<input type="password" id="password" name="password"><br><br>
			<input type="submit" value="Login">
		</form>
	</div>
	`

	let body=document.body
	if(body.innerHTML.includes(add_report_box)){
		body.innerHTML=body.innerHTML.replace(add_report_box,"")+add_report_box
	}
	else{
		body.innerHTML=body.innerHTML+past_record_box;
	}
	
}


function add_report(){
    // document.body
    let past_record_box=`
	<div class="login-box">
		<h1>Check to past reports</h1>
		<form action="/past_records" method="POST">
			<label for="username">User ID:</label>
			<input type="text" id="username" name="username"><br><br>
			<label for="password">Password:</label>
			<input type="password" id="password" name="password"><br><br>
			<input type="submit" value="Login">
		</form>
	</div>
	`

	let add_report_box=`
	<div class="login-box">
		<h1>Check to Add reports</h1>
		<form action="/add_report_doctor_check" method="POST">
			<label for="username">User ID:</label>
			<input type="text" id="username" name="username"><br><br>
			<label for="password">Password:</label>
			<input type="password" id="password" name="password"><br><br>
			<input type="submit" value="Login">
		</form>
	</div>
	`

	body=document.body

	if(body.innerHTML.includes(past_record_box)){
		body.innerHTML=body.innerHTML.replace(past_record_box,"")+past_record_box
	}
	else{
		body.innerHTML=body.innerHTML+add_report_box;
	}
}


function no_user(){
	let body= document.body
	message="<p>No such user found<p>"
	body.innerHTML=body.innerHTML+message
}

