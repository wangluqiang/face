#coding=utf-8
import os,sys
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
import DMExceptions
from FacePerson import FacePerson
from FaceDB import FaceDB
from FaceDevice import FaceDevice
from FaceMatch import FaceMatch
from FacePre import FacePre
from FaceVideo import FaceVideo

def handle_exception(func):
	def _handle_exception(args):
		try:
			func(args)
		except DMExceptions.GetHttpResponseError as ex:
			args.fail("get response from server error!")
		except DMExceptions.ResposeToJsonException as ex:
			args.fail("the facedb add response is not a standard json format!")
		except DMExceptions.ConnectException as ex:
			args.fail("thrift连接失败")
		except DMExceptions.RequestVideoDetectInitException as ex:
			args.fail("RequestVideoDetect初始化失败!")
		except DMExceptions.RequestVideoDetectCloseException as ex:
			args.fail("RequestVideoDetect关闭失败!")
		except DMExceptions.NoneTransportClose as ex:
			args.fail("无thrift连接需要关闭,但仍然执行关闭操作！")
		except DMExceptions.SendException as ex:
			args.fail("thrift建立连接后，发送数据出现问题")
		except DMExceptions.DBInitException as ex:
			args.fail("connect to database fail!")
		except DMExceptions.DBNoneQueryException as ex:
			args.fail("查询时数据库连接异常！")
		except DMExceptions.DBQueryException as ex:
			args.fail("查询数据库失败!")
		except DMExceptions.NoDBQueryResultException as ex:
			args.fail("查询数据库无信息！")
		except DMExceptions.DBNoneCloseException as ex:
			args.fail("关闭数据库时无数据库连接！")
		except DMExceptions.DBCloseException as ex:
			args.fail("关闭数据库时失败！")
		except DMExceptions.FacePicRetrievalInitException as ex:
			args.fail("FacePicRetrieval初始化失败！")
		except DMExceptions.FacePicRetrievalCloseException as ex:
			args.fail("FacePicRetrieval的thrift连接关闭失败！")
		except DMExceptions.ReadPicException as ex:
			args.fail("读取照片失败！")
		finally:
			#后期再完善
			if 'db' in args.items.keys():
				args.items['db'].close()
			if 'compare' in args.items.keys():
				args.items['compare'].close()
			if  'person' in args.items.keys():
				fp = FacePerson()
				if type(args.items["person"]) == list:
					for person in args.items['person']:
						fp.faceperson_delete(p_id=person['errorinfo'])
				else:
					fp.faceperson_delete(p_id=args.items["person"]["errorinfo"])
			if 'facedb' in args.items.keys():
				fd = FaceDB()
				if isinstance(args['facedb'],list):
					for f in args['facedb']:
						fd.facedb_delete(face_id=f['errorinfo'])
				else:
					fd.facedb_delete(face_id=args.items['facedb']["errorinfo"])
			if "facedevice" in args.items.keys():
				facedevice = FaceDevice()
				if isinstance(args.items['facedevice']):
					for device in args.items['facedevice']:
						facedevice.facedevice_delete(device_id=device['errorinfo'])
				else:
					facedevice.facedevice_delete(device_id=args.items['facedevice']['errorinfo'])
			if "match" in args.items.keys():
				match = FaceMatch()
				if isinstance(args.items['match'],list):
					for m in args.items['match']:
						match.facematch_delete(m_id=m['errorinfo'])
				else:
					match.facematch_delete(m_id=args.items['match']['errorinfo'])
			if "preprocess" in args.items.keys():
				pre = FacePre()
				if isinstance(args['preprocess'],list):
					for p in args['preprocess']:
						pre.facepre_delete(p_id=p['errorinfo'])
				else:
					pre.facepre_delete(p_id=args.items['preprocess']['errorinfo'])
			if "video" in args.items.keys():
				video = FaceVideo()
				if type(args.items["video"]) == list:
					for v in args.items["video"]:
						video.facevideo_delete(id=v["video_id"])
				else:
					video.facevideo_delete(id=args.items['video']['video_id'])
	return _handle_exception