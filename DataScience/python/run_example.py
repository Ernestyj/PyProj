# -*- coding: utf-8 -*-
import json

if __name__ == '__main__':
    str = '''
set_parser rpds_parser("./schema/EVALRESOLUTIONCHANNEL_meta.txt"); #do not modify this line


BEGIN{
    print ('channel_name;country;is_logged_out;intent_description;intent_id;channels_offered;Count' );
}

$channels_list = split( ACT.channels_offered , '|');
$channel_dict = new(dict);

for ($ch_info in $channels_list){
    $ch = split( $ch_info , '^') ; 
    
    $Nm = substr($ch[0], 12 ) ; # ChannelName
    $Rk = substr($ch[2], 12 ) ; #ChannelRank
    insert($channel_dict, $Rk, $Nm);
    
    }   
    
$channels_str = '' ;
$Rank_list = ['1', '2', '3', '4', '5'];

for ($Rk in $Rank_list ){
    if ($channel_dict[$Rk] != NULL){
        $channels_str = $channels_str + ','  + $channel_dict[$Rk] ; 
    }
}

$channels_str = substr($channels_str, 1) ;
#$act_str = ACT.channels_offered; 

select count() as $cnt_tot; 
select count() group by CS.intent_desc, CS.intent_id, CS.channel_name,U1.country_from_profile, U1.is_logged_out, $channels_str as $cnt; 

END{
    for($cg in $cnt) {   
        if ( $cg[0] != '' || $cg[1] != '' || $cg[2] != ''){
            $cnt_intent = '' ;
            if ( $cnt[$cg]!= NULL){  $cnt_intent = $cnt[$cg] ; }
            print("%s;%s;%s;%s;%s;%s;%d", $cg[2],$cg[3], $cg[4], $cg[0], $cg[1],$cg[5], $cnt_intent);
        }
    }
}
    '''
    theJson = json.dumps(str)
    print(theJson)