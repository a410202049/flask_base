//假定字符串的每节数都在5位以下
var versionfunegt = function (ver1,ver2) {
    var version1pre = parseFloat(ver1);
    var version2pre = parseFloat(ver2);
    var version1next =  ver1.replace(version1pre + ".","");
    var version2next =  ver2.replace(version2pre + ".","");
    if(version1pre > version2pre){
        return true;
    }else if(version1pre < version2pre){
        return false;
    }else{
        if(version1next >= version2next){
            return true;
        }else{
            return false;
        }
    }
}
// var a="2.2.3";b="2.1.15";
// cpr_version(a,b);