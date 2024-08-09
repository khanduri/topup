import React, { ChangeEventHandler, useEffect } from "react";

import SVGBalance from "images/icons/coins";
import SVGUsage from "images/icons/bars";
import SVGActivity from "images/icons/activity";
import ModalAddMoney from "components/modal/add_money";
import ModalVerifyUser from "components/modal/action_verified";

export function BalanceCard(props: any) {
  const { userSummary, forceFetchCtr, setForceFetchCtr } = props;

  const [displayBalance, setDisplayBalance] = React.useState(0);

  useEffect(() => {
    const currentBalance =
      userSummary && userSummary.user_state && userSummary.user_state.data
        ? userSummary.user_state.data.balance || 0
        : ".";
    setDisplayBalance(currentBalance);
  }, [userSummary, forceFetchCtr]);

  return (
    <div className="relative p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg">
      <div className="flex items-start justify-between">
        <div className="flex flex-col space-y-2">
          <span className="text-gray-400">Current Balance</span>
          <span className="text-lg font-semibold">{displayBalance} AED</span>

          <ModalAddMoney
            currentBalance={displayBalance}
            forceFetchCtr={forceFetchCtr}
            setForceFetchCtr={setForceFetchCtr}
          />
        </div>
        <div className="p-6 bg-gray-100 rounded-md text-4xl">
          <SVGBalance className="text-gray-500 h-12 w-12 " />
        </div>
      </div>
      <div className="absolute -top-3 -right-3">
        <ModalVerifyUser
          verified={
            userSummary && userSummary.user_state && userSummary.user_state.data
              ? userSummary.user_state.data.verified
              : null
          }
          forceFetchCtr={forceFetchCtr}
          setForceFetchCtr={setForceFetchCtr}
        />
      </div>
    </div>
  );
}

export function UsageCard(props: any) {
  const { userSummary } = props;
  if (!userSummary) {
    return <></>;
  }

  const usages = userSummary.user_activities.filter(
    (item: any) => item.data.action === "BENEFICIARY_CREDIT"
  );

  const total_usage = usages.reduce(
    (value: number, item: any) => value + item.data.action_data.amount,
    0
  );
  return (
    <div className=" p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg">
      <div className="flex items-start justify-between">
        <div className="flex flex-col space-y-2">
          <span className="text-gray-400">Month's Usage</span>
          <span className="text-lg font-semibold">
            {userSummary ? total_usage : "."} {" AED"}
          </span>
          <span className="text-sm text-gray-400">
            {3000 - total_usage} AED left
          </span>
        </div>
        <div className="p-6 bg-gray-100 rounded-md text-4xl">
          <SVGUsage className="text-gray-500 h-12 w-12 " />
        </div>
      </div>
    </div>
  );
}

export function ActivityCard(props: any) {
  const { userSummary } = props;
  if (!userSummary) {
    return <></>;
  }
  const credits = userSummary.user_activities.filter(
    (item: any) => item.data.action === "BENEFICIARY_CREDIT"
  );
  const balance_adds = userSummary.user_activities.filter(
    (item: any) => item.data.action === "BALANCE_ADD"
  );

  return (
    <div className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg">
      <div className="flex items-start justify-between">
        <div className="flex flex-col space-y-2">
          <span className="text-gray-400">Activity</span>
          <span className="text-sm text-gray-400">
            <span className="text-lg font-semibold text-gray-700">
              {userSummary ? credits.length : "."}
            </span>
            {" topups"}
          </span>
          <span className="text-sm text-gray-400">
            <span className="text-lg font-semibold text-gray-700">
              {userSummary ? balance_adds.length : "."}
            </span>
            {" balance adds"}
          </span>
        </div>
        <div className="p-6 bg-gray-100 rounded-md text-4xl">
          <SVGActivity className="text-gray-500 h-12 w-12 " />
        </div>
      </div>
    </div>
  );
}
