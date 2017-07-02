<?php
// Check for empty fields
if(empty($_POST['name'])      ||
   empty($_POST['email'])     ||
   empty($_POST['tel'])     ||
   empty($_POST['content'])   ||
   !filter_var($_POST['email'],FILTER_VALIDATE_EMAIL))
   {
   echo "No arguments Provided!";
   return false;
   }
   
$name = strip_tags(htmlspecialchars($_POST['name']));
$email_address = strip_tags(htmlspecialchars($_POST['email']));
$tel = strip_tags(htmlspecialchars($_POST['tel']));
$content = strip_tags(htmlspecialchars($_POST['content']));
   
// Create the email and send the message
$to = 'tingyu12345@gmail.com'; // Add your email address inbetween the '' replacing yourname@yourdomain.com - This is where the form will send a message to.
$email_subject = "[White House]有訪客留言:  $name";
$email_body = "留言資料明細:\n\n姓名: $name\n\nEmail: $email_address\n\n連絡電話: $tel\n\n留言內容:\n$content";
$headers = "From: noreply@superwhite.ml\n"; // This is the email address the generated message will be from. We recommend using something like noreply@yourdomain.com.
$headers .= "Reply-To: $email_address";   
mail($to,$email_subject,$email_body,$headers);
return true;         
?>
