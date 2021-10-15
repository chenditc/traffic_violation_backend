import { useState, useCallback } from "react";
import { IEvent } from "./event-list";
import { request } from "umi";
export default function ReportEditorModel () {
  const [ reportInfo, setReportInfo ] = useState({} as IEvent);
  const setViolationType = useCallback(
    (type: string) => {
      setReportInfo(info => ({
        ...info,
        violation_type: type
      }))
    },
    [setReportInfo],
  );
  const setPlateNumber = useCallback(
    (plateNumber: string) => {
      setReportInfo(info => ({
        ...info,
        plate_num: plateNumber
      }))
    },
    [setReportInfo],
  );
  const onSubmit = useCallback(
    () => {
      request("https://traffic-violation.azurewebsites.net/api/save_report_info", {
        method: "post",
        body: JSON.stringify({
          "user": reportInfo["tel"],
          "report_json": JSON.stringify(reportInfo)
        })
      })
    },
    [reportInfo],
  )
  return {
    reportInfo,
    setReportInfo,
    setViolationType,
    setPlateNumber,
    onSubmit
  }
}