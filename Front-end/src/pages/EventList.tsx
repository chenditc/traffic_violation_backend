import { Card, WingBlank, WhiteSpace } from "antd-mobile";
import { useMemo, useEffect, useCallback } from "react";
import { useModel, history } from "umi";
import styles from "@/pages/index.less";
import { IEvent } from "@/models/event-list";
export default function EventListPage () {
  const { eventList, fetchList } = useModel("event-list");
  useEffect(() => {
    fetchList("17602144419");
  }, []);
  const onClickItem = useCallback(
    (reportId) => () => {
      history.push(`/report?id=${reportId}`)
    },
    [history],
  )
  const eventCardList = useMemo(() => {
    return eventList.map((item: IEvent) => {
      return (
        <div key={item.report_id}>
        <WhiteSpace size="lg"/>
        <Card onClick={onClickItem(item.report_id)}>
          <Card.Header title={item.loc_desp}/>
          <Card.Body>
            <img src={item.video_info.cover.url} className={styles.cover}/>
          </Card.Body>
          <Card.Footer content={item.time_str}/>
        </Card>
        </div>
      )
    })
  }, [eventList])
    return (
        <WingBlank size="lg">
        {eventCardList}
        </WingBlank>
    )
};