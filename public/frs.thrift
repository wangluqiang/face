//Client Interface
struct client_conf
{
    1:byte    msg_type,
    2:i32     client_id,
    3:string  client_name,
    4:string  client_ip,
    5:i16     client_port,
    6:byte    match_type,
    7:byte    camera_type,
    8:string  camera_ip,
    9:i16     camera_port,
    10:string camera_user,
    11:string camera_pwd,
    12:byte   card_type,
    13:i16    face_no,
    14:double threshold,
    15:string match_ip,
    16:i16    match_port,
}

//Match Interface
//比对端与Server端消息类型：
//Typedef  enum  match_msg_type
//{
//    E_MATCH_MSG_TYPE_INIT = 0,
//    E_MATCH_MSG_TYPE_MODIFY,
//    E_MATCH_MSG_TYPE_DEL,
//    E_MATCH_MSG_TYPE_FACEDB_ADD,
//    E_MATCH_MSG_TYPE_FACEDB_MODIFY,
//    E_MATCH_MSG_TYPE_FACEDB_DEL,
//    E_MATCH_MSG_TYPE_PERSON_ADD,
//    E_MATCH_MSG_TYPE_PERSON_MODIFY,
//    E_MATCH_MSG_TYPE_PERSON_DEL,
//}

struct SearchPicInfo
{
    1:i32 p_id
    2:i32 face_db;
    3:double score;
}

struct ClientInMsgPicSearch
{
    1:string uuid,
    2:binary pic,
    3:i32    face_no,//0为全库检索
    4:double threshold,
    5:i32    pic_num,
}

struct PicSerchReturn
{
    1:list<SearchPicInfo> info,
    2:i32 success_flag,
}

struct SearchGrabPicInfo
{
    1:i32 grab_id,
    2:i32 c_id,
    3:double score,
    4:string time,
}

struct PicSearchInGrab
{
    1:string uuid,
    2:binary pic,
    3:list<i32> c_id,
    4:list<string> time,
    5:double  score,
    6:i32    pic_num,
}

struct GrabPicSearchReturn
{
    1:list<SearchGrabPicInfo>  info,
    2:i32  success_flag,
}

struct GetPicFeatureAndSmallPicIn
{
    1:string uuid,
    2:binary pic,
    3:i32    pic_size,
}

struct GetPicFeatureAndSmallPicReturn
{
    1:string uuid,
    2:binary pic,
    3:i32    pic_size,
    4:binary feature,
    5:i32    success_flag,
}

struct alarm_conf
{
    1:i32  alarm_id,
    2:string alarm_ip,
    3:i16 alarm_port,
    4:list<i32>	c_id_list,
}

struct match_conf
{
    1:byte     msg_type,
    2:string   match_name,
    3:string   match_ip,
    4:i16      match_port,
    5:i16      face_no,
    6:double   threshold,
    7:i32      clients_max,
    8:string   sql_addr,
    9:i16      sql_port,
    10:string  sql_user,
    11:string  sql_pwd,
    12:string  match_result_table,
    13:string  grab_face_table,
    14:string  face_no_table,
    15:i32     person_no,
    16:string  person_name,
    17:string  person_id,
    18:binary  feature,
    19:binary  face_pic,
    20:string  db_name,
    21:string  person_table,
    22:list<alarm_conf> alarm_config_info,
    23:i32     success_flag,
}

//Preprocess Interface
//Typedef  enum  msg_type
//{
//    E_TYPE_INIT = 1,
//    E_TYPE_ADD_HOST  = 2,
//    E_TYPE_DEL_HOST  = 3,
//    E_TYPE_UPDATE_HOST  = 4,
//    E_TYPE_ADD_CHANNEL  = 5,
//    E_TYPE_DEL_CHANNEL  = 6,
//    E_TYPE_MOD_MATCH    = 7,
//}

struct net_video_in_conf
{
    1:string   ip,
    2:i32      port,
}

struct net_video_channel
{
    1:i32      device_id,
		2:i32      channel_dev_id,
    3:i32      channel_no,
    4:string   channel_name,
    5:i32      connect_mode,
    6:list<i32> face_db_no,
}

struct net_video_host
{
    1:i32      msg_type,
    2:i32      type,
    3:i32      device_id,
    4:string   ip,
    5:i32      port,
    6:string   user,
    7:string   pwd,
    8:list<net_video_channel> channels,
}

struct net_video_conf
{
    1:list<net_video_host> hosts,
    2:string  match_ip,
    3:i32     match_port,
    4:i32     cap_interval,
    5:i32     cap_type,
    6:i32     success_flag,
    7:string  err_msg,
}

struct match_info
{
		1:i32     msg_type,
    2:string  match_ip,
    3:i32     match_port,
}

//Alarm Interface
struct alarm
{
    1:byte msg_type,//0 告警端初始化
    2:i32  alarm_id,
    3:string alarm_ip,
    4:i16 alarm_port,
    5:list<i32>	c_id_list,
    6:i32 success_flag,
}

service frs_server
{
    match_conf match_config(1:match_conf req1),
    GetPicFeatureAndSmallPicReturn get_pic_feature_and_small_pic(1:GetPicFeatureAndSmallPicIn req1),
    GrabPicSearchReturn request_grabpic_search(1:PicSearchInGrab req1),
    PicSerchReturn request_pic_search(1:ClientInMsgPicSearch req1),
    net_video_conf init(1:net_video_in_conf conf),
    i32 net_video_config_host(1:i32 type, 2:net_video_host req),
    i32 set_match_info(1:match_info info),
    alarm alarm(1:alarm req1),//alarm增删改查
    client_conf client_config(1:client_conf req2),
}