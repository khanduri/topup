import Gravatar from "react-gravatar";

import ModalActionTopUp from "components/modal/action_topup";
import ModalActionActivateBeneficiary from "components/modal/action_activate";

export default function Component(props: any) {
  const { beneficiaries, forceFetchCtr, setForceFetchCtr } = props;

  if (!beneficiaries) {
    return <></>;
  }

  return (
    <>
      {beneficiaries.map((member: any, idx: number) => (
        <tr
          key={idx}
          className={
            "transition-all " +
            (member.data.active
              ? " hover:shadow-lg hover:bg-indigo-50 "
              : " bg-gray-50 ")
          }
        >
          <td className="px-6 py-4 whitespace-nowrap">
            <div className="flex items-center">
              <div className="relative flex-shrink-0 w-10 h-10">
                {member.data.active ? (
                  ""
                ) : (
                  <span className="opacity-85 absolute -top-3 -right-3 bg-slate-400 text-slate-50 p-2 text-xs rounded ml-1">
                    inactive
                  </span>
                )}
                <Gravatar email={member.data.email} default="identicon" />
              </div>
              <div className="ml-4">
                <div className="text-sm font-medium text-gray-900">
                  {member.data.nickname}
                </div>
                <div className="text-sm text-gray-500">{member.data.email}</div>
              </div>
            </div>
          </td>
          <td className="px-6 py-4 whitespace-nowrap">
            <div
              className={
                "text-sm " +
                (member.data.active && member.data.balance <= 50
                  ? " animate-bounce text-red-500  "
                  : " text-gray-500  ")
              }
            >
              {member.data.balance} AED
            </div>
          </td>

          <td className="px-6 py-4 text-xs font-semibold text-center whitespace-nowrap">
            {member.data.active ? (
              <ModalActionTopUp
                beneficiary={member}
                forceFetchCtr={forceFetchCtr}
                setForceFetchCtr={setForceFetchCtr}
              />
            ) : (
              ""
            )}
          </td>
          <td className="px-6 py-4 whitespace-nowrap">
            <span className="inline-flex text-xs font-semibold leading-5 ">
              <ModalActionActivateBeneficiary
                beneficiary={member}
                forceFetchCtr={forceFetchCtr}
                setForceFetchCtr={setForceFetchCtr}
              />
            </span>
          </td>
        </tr>
      ))}
    </>
  );
}
