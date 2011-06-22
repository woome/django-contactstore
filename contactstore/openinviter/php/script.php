<?php
$script_loc = dirname(__FILE__) . "/OpenInviter/openinviter.php";
include($script_loc);
$inviter=new OpenInviter();
$oi_services=$inviter->getPlugins();

$provider = $argv[3];
$inviter->startPlugin($provider);
$internal_error = $inviter->getInternalError();
if ($internal_error) {
   echo "error: " . $internal_error;
}
else {
   if (!$inviter->login($argv[1],$argv[2])) {
      $internal_error = $inviter->getInternalError();
      if ($internal_error) {
         echo "error: " . $internal_error;
      }
      else {
         echo "error: login error\n";
      }
   }
   else {
     $contacts=$inviter->getMyContacts();
     foreach ($contacts as $contact => $name) {
        if ($contact == $contacts[$contact]) {
          echo $contact . ",\n";
        }
        else {
          echo $contact . "," . $contacts[$contact] . "\n";
        }
     }
   }
}
?>
