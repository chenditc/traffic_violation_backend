import { Card, Space } from "antd-mobile";
import { useMemo, useEffect, useCallback } from "react";
import { useModel, history } from "umi";
import styles from "@/pages/index.less";
import { IEvent } from "@/models/event-list";
import {
  CheckCircleOutline,
  ExclamationCircleOutline,
} from "antd-mobile-icons";
export default function EventListPage() {
  const { eventList, fetchList } = useModel("event-list");
  useEffect(() => {
    fetchList("17602144419");
  }, []);
  const onClickItem = useCallback(
    (reportId) => () => {
      history.push(`/report?id=${reportId}`);
    },
    [history],
  );
  const eventCardList = useMemo(() => {
    return eventList.map((item: IEvent) => {
      return (
        <Card
          onClick={onClickItem(item.report_id)}
          title={item.loc_desp}
          className={styles["event-card"]}
          headerClassName={styles["event-card-title"]}
        >
          <img src={item.video_info.cover.url} className={styles.cover} />
          <div className={styles["card-footer"]}>
            <span className={styles["time-str"]}>{item.time_str}</span>
            <span>
              {item.report_success ? (
                <CheckCircleOutline />
              ) : (
                <ExclamationCircleOutline />
              )}
            </span>
            {/* TODO footer部分的垂直居中对齐；icon的颜色区分，文字说明 */}
          </div>
        </Card>
      );
    });
  }, [eventList]);
  return (
    <Space direction="vertical" className={styles["event-list"]}>
      {eventCardList}
    </Space>
  );
}
