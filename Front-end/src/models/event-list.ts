import { useCallback, useState } from "react";
import { request } from "umi";
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
  report_success?: boolean;
  plate_candidate_list?: string[];
  report_success_reason?: string[];
}

export default function useEventListModel() {
  const [eventList, setEventList] = useState<IEvent[]>([]);
  const [fetching, setFetching] = useState(false);
  const fetchList = useCallback((userId) => {
    setFetching(true);
    request(
      "https://traffic-violation.azurewebsites.net/api/list_report_info",
      {
        method: "get",
        params: { user: userId },
      },
    ).then((val) => {
      console.log(val);
      setEventList(val);
      setFetching(false);
    });
  }, []);
  return {
    eventList,
    fetchList,
    fetching,
  };
}
