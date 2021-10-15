import { useState, useCallback } from "react";
import { IEvent } from "./event-list";
import { request, history } from "umi";
import { Toast } from "antd-mobile";
export default function ReportEditorModel() {
  const [reportInfo, setReportInfo] = useState({} as IEvent);
  const [submitting, setSubmitting] = useState(false);
  const setViolationType = useCallback(
    (type: string) => {
      setReportInfo((info) => ({
        ...info,
        violation_type: type,
      }));
    },
    [setReportInfo],
  );
  const setPlateNumber = useCallback(
    (plateNumber: string) => {
      setReportInfo((info) => ({
        ...info,
        plate_num: plateNumber,
      }));
    },
    [setReportInfo],
  );
  const onSubmit = useCallback(() => {
    setSubmitting(true);
    request(
      "https://traffic-violation.azurewebsites.net/api/save_report_info",
      {
        method: "post",
        body: JSON.stringify({
          user: reportInfo["tel"],
          report_json: JSON.stringify(reportInfo),
        }),
      },
    )
      .then(() => {
        setSubmitting(false);
        Toast.show({
          icon: "success",
          content: "举报成功",
        });
        history.push("/list");
      })
      .catch((err) => {
        setSubmitting(false);
        Toast.show({
          icon: "fail",
          content: "举报信息有误",
        });
        return;
      });
  }, [reportInfo]);
  return {
    reportInfo,
    setReportInfo,
    setViolationType,
    setPlateNumber,
    onSubmit,
    submitting,
  };
}
