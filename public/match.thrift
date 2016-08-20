//比对端与client端消息类型：
//Typedef  enum  match_msg_type
//{
//    E_CLIENT_MSG_TYPE_1_N = 0,
//    E_CLIENT_MSG_TYPE_1_1,
//    E_CLIENT_MSG_TYPE_GET_INFO_BY_ID,
//    E_CLIENT_MSG_TYPE_GET_PIC_FEATURE,
//}

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

//比对端与client端通信消息格式：
struct ClientInMsg1vN
{
    1:i32    msg_type,
    2:i32    dev_id,
    3:string uuid,
    4:binary pic,
    5:i32    pic_size,
    6:i32    max_face,
    7:i32    dbno,
}

struct ClientInMsg1v1
{
    1:i32    face_no,
    2:i32    type,
    3:i32    dev_id,
    4:string uuid,
    5:binary pic,
    6:i32    pic_size,
    7:binary feature,
    8:string cap_uuid,
    9:binary cap_pic,
    10:i32   cap_pic_size,
    11:string person_id,
    12:string person_name,
    13:double threshold,
    14:i32   is_last,
}

struct MatchPicReturn
{
    1:i32    msg_type,
    2:i32    match_type,
    3:i32    left,
    4:i32    top,
    5:i32    right,
    6:i32    bottom,
    7:string person_id,
    8:string person_name,
    9:binary db_pic,
    10:i32   db_pic_size,
    11:i32   face_db,
    13:i32   success_flag,
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

struct GetPersonInfoByIDOut
{
    1:i32    person_no,
    2:string person_id,
    3:string person_name,
    4:string uuid,
    5:binary pic,
    6:i32    pic_size,
    7:binary feature, 
    8:i32    success_flag,   
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

struct ClientInMsgPicSearch
{
    1:string uuid,
    2:binary pic,
    3:i32    face_no,//0为全库检索
    4:double threshold,
    5:i32    pic_num,
}

struct SearchPicInfo
{
    1:i32 p_id
    2:i32 face_db;
    3:double score;
}

struct PicSerchReturn
{
		1:list<SearchPicInfo> info,
		2:i32 success_flag,
}

struct ClientInMsgVideoDetect
{
    1:i32    msg_type,
    2:i32    c_id,
    3:string uuid,
    4:binary pic,
    5:i32    pic_size,
    6:i32    max_face,
    7:list<i32>    face_db_list,
}

struct alarm_info
{
    1:i32 r_id,
    2:string res1,
    3:string res2,
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

service frs_match
{
    MatchPicReturn request_1_1(1:ClientInMsg1v1 req1),
    list<MatchPicReturn> request_1_N(1:ClientInMsg1vN req1),
    i32 request_video_detect(1:ClientInMsgVideoDetect req1),
    GetPicFeatureAndSmallPicReturn get_pic_feature_and_small_pic(1:GetPicFeatureAndSmallPicIn req1),
    GetPersonInfoByIDOut get_person_info_by_id(1:string id),
    match_conf match_config(1:match_conf req1),
    PicSerchReturn request_pic_search(1:ClientInMsgPicSearch req1),
    i32 push_alarm(1:alarm_info req1),//match推送比对结果给alarm
    GrabPicSearchReturn request_grabpic_search(1:PicSearchInGrab req1),
}

