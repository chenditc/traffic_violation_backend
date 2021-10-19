import { history, useModel } from "umi";
import { useMemo, useCallback, useEffect, useState } from "react";
import { List, Picker, Button } from "antd-mobile";
import { IEvent } from "@/models/event-list";
import { AutoComplete, Input as AntdInput } from "antd";
import styles from "@/pages/index.less";
const Item = List.Item;
const violationTypes = [
  "加塞（遇前方机动车停车排队时，借道超车或者占用对面车道、穿插等候车辆的）",
  "变道、转弯、掉头、靠边、起步时不打灯（不按规定使用转向灯）",
  "实线变道（违反禁止标线指示）",
  "转弯不让直行（转弯车不让直行车或行人）",
  "黄实线停车（违反禁止标线指示）",
  "连续变换两条车道（驾驶机动车一次连续变换两条车道）",
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
  "逆向行驶（机动车逆向行驶的）",
  "车窗抛物（向道路上抛洒物品）",
  "压斑马线（违反禁止标线指示）",
  "货车上高架（违反禁令标志指示）",
  "机动车载物行驶时遗撒、飘散载运物",
  "机动车载货长度、宽度、高度超过规定",
  "占用应急车道（占用应急车道行驶的）",
  "不按导向车道行驶（不按导向车道行驶）",
  "占用公交车道（机动车违规使用专用车道）",
  "货车占客车道（机动车违规使用专用车道）",
  "路口滞留（交通拥堵处不按规定停车等候）",
  "开车打电话（驾车时拨打接听手持电话的）",
  "不避让特种车辆（不避让执行任务特种车辆）",
  "不在机动车道内行驶（机动车不走机动车道）",
  "危险路段掉头（在容易发生危险的路段掉头的）",
  "闯红灯（驾驶机动车违反道路交通信号灯通行的）",
  "未避让行人（遇行人正在通过人行横道时未停车让行的）",
  "违反规定掉头（在禁止掉头或者禁止左转弯标志、标线的地点掉头的）",
  "红灯时超越停车线（通过路口遇停止信号时，停在停止线以内或路口内的）",
  "拥堵时在人行横道、网格线内停车（遇前方机动车停车排队等候或者缓慢行驶时，在人行横道、网状线区域内停车等候的）",
];
const violationPickerData = violationTypes.map((item) => ({
  label: item,
  value: item,
}));
export default function ReportPage() {
  const query = history.location.query;
  const { eventList } = useModel("event-list");
  console.log(eventList, "2222");
  if (!query || eventList.length === 0) {
    history.push("/list");
  }
  const {
    reportInfo: editedInfo,
    setReportInfo,
    setViolationType,
    setPlateNumber,
    onSubmit,
    submitting,
  } = useModel("report-editor");
  const reportInfo: IEvent | undefined = eventList.find(
    (item) => item.report_id === query!.id,
  );

  useEffect(() => {
    setReportInfo(reportInfo as IEvent);
  }, [reportInfo]);
  const [typePickerVisibile, setTypePickerVisibile] = useState<boolean>(false);

  const plateNumberCandidates = useMemo(() => {
    if (reportInfo?.plate_candidate_list) {
      return reportInfo.plate_candidate_list.map((item) => ({
        label: item,
        value: item,
      }));
    } else {
      return [];
    }
  }, [reportInfo]);
  const reportHistory = useMemo(() => {
    if (reportInfo?.report_success_reason) {
      return reportInfo.report_success_reason.map((item, index) => (
        <Item key={index}>
          <div style={{ fontSize: "13px", color: "#575757" }}>{item}</div>
        </Item>
      ));
    }
  }, []);

  const onViolationChange = useCallback(
    (val) => {
      setViolationType(val[0]);
    },
    [setViolationType],
  );
  const onPlateNumberChange = useCallback(
    (val) => {
      console.log("1111", val);
      setPlateNumber(val);
    },
    [setPlateNumber],
  );
  // TODO need validation?
  // const onClickSubmit = useCallback(() => {
  //   onSubmit();
  // }, [onSubmit]);
  return (
    <div>
      <List mode="card">
        <div className={styles["basic-info"]}>
          <span>基础信息</span>
          <a href={reportInfo?.video_info.cover.url} target="_blank">
            <img
              src={reportInfo?.video_info.cover.url}
              style={{ width: "100%" }}
            />
          </a>
        </div>
        <Item title="视频地址"><a href={reportInfo?.video_info.video.url} target="_blank">点击播放</a></Item>
        <Item title="地点"><a href={'https://uri.amap.com/marker?position=' + reportInfo?.gcj_lng + ',' + reportInfo?.gcj_lat} target="_blank">{reportInfo?.loc_response.GaoDeMiaoShu}</a></Item>
        <Item title="时间">{reportInfo?.time_str}</Item>
        <Item title="手机号">{reportInfo?.tel}</Item>
      </List>
      {reportInfo?.report_success_reason &&
        reportInfo.report_success_reason.length > 0 && (
          <List mode="card">
            <div className={styles["basic-info"]}>
              <span>举报历史</span>
            </div>
            {reportHistory}
          </List>
        )}
      <List mode="card">
        <div className={styles["basic-info"]}>
          <span>确认举报信息</span>
        </div>
        <Item title="车牌号">
          <AutoComplete
            options={plateNumberCandidates}
            value={editedInfo.plate_num}
            onSelect={onPlateNumberChange}
            style={{ width: "100%" }}
          >
            <AntdInput
              size="large"
              placeholder="请输入"
              className={styles["plate-input"]}
              onChange={(ev) => {
                onPlateNumberChange(ev.target.value);
              }}
              value={editedInfo.plate_num}
            />
          </AutoComplete>
        </Item>
        <Item title="违章类型" arrow>
          <Picker
            columns={[violationPickerData]}
            visible={typePickerVisibile}
            onClose={() => {
              setTypePickerVisibile(false);
            }}
            value={[editedInfo.violation_type || ""]}
            onConfirm={onViolationChange}
            key={"violation"}
          />
          <div
            style={{ marginTop: "5px", width: "80%" }}
            onClick={() => {
              setTypePickerVisibile(true);
            }}
          >
            {editedInfo.violation_type ? editedInfo.violation_type : "请选择"}
          </div>
        </Item>
      </List>
      <Button
        onClick={onSubmit}
        className={styles["login-button"]}
        loading={submitting}
      >
        {!reportInfo?.report_success ? "提交举报!" : "再举报!"}
      </Button>
    </div>
  );
}
