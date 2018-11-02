<?php
 
$cookie_name = $cookie_val = '';
 
$lines = file(dirname(__FILE__).'/id.txt');
foreach($lines as $line){
    list($username, $password) = explode('#', $line);
    $username = trim($username);
    $password = trim($password);
 
    if(empty($username) || empty($password)){
        continue;
    }
 
    $suburl = "https://www.hostloc.com/member.php?mod=logging&action=login";
    $loginInfo = array(
            "username" => $username,
            "password" => $password,
            "fastloginfield" => "username",
            "quickforward" => "yes",
            "handlekey" => "ls",
            "loginsubmit" => true
    );
 
    echo "login($username) ... ";
    $login = curl_post($suburl,$loginInfo);
 
    if(strpos($login, $username) !== FALSE){
 
        preg_match("/>用户组: (.*?)<\/a>/", $login, $preg);
        $group = $preg[1];
        echo "Success!($group)\n";
    }else{
        echo "Failed!\n\n";
        continue;
    }
 
    extract(get_jf());
    echo "Credit: $credit; Money: $money\n";
 
    echo "Visting user space ";
    for($i=0;$i<20;$i++){
        $uid = rand(0,30000);
        curl_get($spaceUrl = "https://www.hostloc.com/space-uid-{$uid}.html");
        echo ".";
    }
    echo " done!\n";
    extract(get_jf());
    echo "Credit: $credit; Money: $money\n\n";
 
 
}
 
function get_jf(){
    $data = array();
    $html = curl_get('https://www.hostloc.com/home.php?mod=spacecp&ac=credit&op=base');
    preg_match("/积分: (\d+)<\/a>/", $html, $preg);
    if(!empty($preg[1])){
        $data['credit'] = $preg[1];
    }else{
        $data['credit'] = 0;
    }
    preg_match("/金钱: <\/em>(\d+)/", $html, $preg);
    if(!empty($preg[1])){
        $data['money'] = $preg[1];
    }else{
        $data['money'] = 0;
    }
 
    return $data;
}
 
function curl_post($url, $post_data){
    global $cookie_name, $cookie_val;
    while(true){
        $res = do_curl_post($url, $post_data);
        preg_match("/cookie=\"(\w*?)\=(\w*)/", $res, $preg_cookie);
        preg_match("/href=\"(.*?)\"/", $res, $preg_url);
 
        if(!empty($preg_cookie[1])){
            $cookie_name = $preg_cookie[1];
            $cookie_val = $preg_cookie[2];
            $res = do_curl_post($preg_url[1], $post_data);
        }else{
            break;
        }
        sleep(1);
    }
    return $res;
}
 
 
function do_curl_post($url, $post_data){
    global $cookie_name, $cookie_val;
    $ch = curl_init ();
    curl_setopt($ch, CURLOPT_POST , 1);
    curl_setopt($ch, CURLOPT_HEADER , 0);
    curl_setopt($ch, CURLOPT_URL , $url);
    curl_setopt($ch, CURLOPT_COOKIEJAR , '/tmp/hostloc.cookie');
    //curl_setopt($ch, CURLOPT_HTTPHEADER, array('X-FORWARDED-FOR:'.rand_ip()));
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (compatible;Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)');
    curl_setopt($ch, CURLOPT_POSTFIELDS , $post_data);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_TIMEOUT,600);
    curl_setopt($ch, CURLOPT_REFERER, 'http://www.hostloc.com/');
    if(!empty($cookie_name)){
        curl_setopt($ch, CURLOPT_COOKIE, "$cookie_name=$cookie_val;");
    }
    $result = curl_exec($ch);
    curl_close($ch);
    return $result;
}
 
 
function curl_get($url){
    global $cookie_name, $cookie_val;
    $ch = curl_init ();
    curl_setopt($ch, CURLOPT_HEADER , 0);
    curl_setopt($ch, CURLOPT_URL , $url);
    curl_setopt($ch, CURLOPT_COOKIEFILE, '/tmp/hostloc.cookie');
    //curl_setopt($ch, CURLOPT_HTTPHEADER, array('X-FORWARDED-FOR:'.rand_ip()));
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (compatible;Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)');
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_TIMEOUT,600);
    if(!empty($cookie_name)){
        curl_setopt($ch, CURLOPT_COOKIE, "$cookie_name=$cookie_val;");
    }
    $result = curl_exec($ch);
    curl_close($ch);
    return $result;
}
 
function rand_ip(){
    return rand(1,255).'.'.rand(1,255).'.'.rand(1,255).'.'.rand(1,255);
}
