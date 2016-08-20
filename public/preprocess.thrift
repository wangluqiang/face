//设备类型：
//Typedef  enum  dev_type
//{
//    E_DEV_ONVIF = 0,
//}

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

struct match_conf
{
		1:i32     msg_type,
    2:string  match_ip,
    3:i32     match_port,
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

service net_video_service
{
    net_video_conf init(1:net_video_in_conf conf),
    i32 request_video_detect(1:ClientInMsgVideoDetect req1),
    i32 net_video_config_host(1:i32 type, 2:net_video_host req),
    i32 set_match_info(1:match_conf info),
}

