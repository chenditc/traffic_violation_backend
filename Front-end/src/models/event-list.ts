import { useCallback, useState } from "react";
import {request} from "umi";
interface IMedia {
    url: string;
    verify_content: string;
}
interface IVideoInfo {
    cover: IMedia;
    fileId: string;
    video: IMedia;
}
export interface IEvent {
    lat: number;
    lon: number;
    loc_desp: string;
    report_id: string;
    tel: string;
    time: number;
    time_str: string;
    user_id: string;
    video_info: IVideoInfo; 
    plate_color?: number;
    plate_num?: string;
    violation_type?: string;
}


export default function useEventListModel() {
    const [eventList, setEventList] = useState<IEvent[]>([]);
    const fetchList = useCallback((userId) => {
        request("https://traffic-violation.azurewebsites.net/api/list_report_info", {
            method: "get",
            params: {user: userId}
        }).then((val) => {
            setEventList(val);
        });
    },[])
    return {
        eventList,
        fetchList
    }
}