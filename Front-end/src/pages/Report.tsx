import { history, useModel } from "umi";
import { useMemo, useCallback, useEffect } from "react";
import { List, Input, Picker, Space, Button } from "antd-mobile";
import { IEvent } from "@/models/event-list";
import styles from "@/pages/index.less";
const Item = List.Item;
const violationTypes = [
  "摩托车闯禁令",
  "大型车辆污损、遮挡号牌",
  "机动车噪声污染",
  "驾车时浏览电子设备",
  "摩托车占用公交车道",
  "机动车未按规定交替通行",
  "货车未按规定黏贴反光标志",
  "闯禁令（违反禁令标志指示）",
  "驾驶摩托车时未佩戴安全头盔",
  "路间黄实线处左转或调头（违反禁止标线指示）",
  "实线变道（违反禁止标线指示）",
  "逆向行驶（机动车逆向行驶的）",
  "车窗抛物（向道路上抛洒物品）",
  "压斑马线（违反禁止标线指示）",
  "货车上高架（违反禁令标志指示）",
  "黄实线停车（违反禁止标线指示）",
  "机动车载物行驶时遗撒、飘散载运物",
  "机动车载货长度、宽度、高度超过规定",
  "占用应急车道（占用应急车道行驶的）",
  "不按导向车道行驶（不按导向车道行驶）",
  "变道、转弯、掉头、靠边、起步时不打灯（不按规定使用转向灯）",
  "转弯不让直行（转弯车不让直行车或行人）",
  "占用公交车道（机动车违规使用专用车道）",
  "货车占客车道（机动车违规使用专用车道）",
  "路口滞留（交通拥堵处不按规定停车等候）",
  "开车打电话（驾车时拨打接听手持电话的）",
  "不避让特种车辆（不避让执行任务特种车辆）",
  "不在机动车道内行驶（机动车不走机动车道）",
  "危险路段掉头（在容易发生危险的路段掉头的）",
  "闯红灯（驾驶机动车违反道路交通信号灯通行的）",
  "未避让行人（遇行人正在通过人行横道时未停车让行的）",
  "连续变换两条车道（驾驶机动车一次连续变换两条车道）",
  "违反规定掉头（在禁止掉头或者禁止左转弯标志、标线的地点掉头的）",
  "红灯时超越停车线（通过路口遇停止信号时，停在停止线以内或路口内的）",
  "加塞（遇前方机动车停车排队时，借道超车或者占用对面车道、穿插等候车辆的）",
  "拥堵时在人行横道、网格线内停车（遇前方机动车停车排队等候或者缓慢行驶时，在人行横道、网状线区域内停车等候的）",
];
const violationPickerData = violationTypes.map((item) => ({
  label: item,
  value: item,
}));
export default function ReportPage() {
  const query = history.location.query;
  if (!query) {
    history.push("/list");
  }
  const { eventList } = useModel("event-list");
  const {
    reportInfo: editedInfo,
    setReportInfo,
    setViolationType,
    setPlateNumber,
    onSubmit,
  } = useModel("report-editor");
  const reportInfo: IEvent | undefined = useMemo(() => {
    return eventList.find((item) => item.report_id === query!.id);
  }, [eventList, query]);
  useEffect(() => {
    setReportInfo(reportInfo as IEvent);
  }, [reportInfo]);
  const onViolationChange = useCallback(
    (val) => {
      setViolationType(val[0]);
    },
    [setViolationType],
  );
  const onPlateNumberChange = useCallback(
    (val) => {
      setPlateNumber(val);
    },
    [setPlateNumber],
  );
  const onClickSubmit = useCallback(() => {
    onSubmit();
  }, [onSubmit]);
  return (
    <div>
      <List>
        <img src={reportInfo?.video_info.cover.url} style={{ width: "100%" }} />
        <Item title="地点">{reportInfo?.loc_desp}</Item>
        <Item title="时间">{reportInfo?.time_str}</Item>
        <Item title="手机号">{reportInfo?.tel}</Item>
      </List>
      {/* TODO 找个合适的selector组件，List样式 */}
      {!reportInfo?.report_success && (
        <Button onClick={onSubmit} className={styles["login-button"]}>
          Report now!
        </Button>
      )}
    </div>
  );
}
