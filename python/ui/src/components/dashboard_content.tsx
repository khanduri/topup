import ModalAddBeneficiary from "components/modal/add_beneficiery";
import BeneficiariesTable from "components/beneficiaries_table";

export default function Component(props: any) {
  const { allowedTopups, beneficiaries, forceFetchCtr, setForceFetchCtr } =
    props;

  return (
    <>
      <div className="grid gap-5 mt-6 grid-cols-1">
        <div className="border-t">
          <div className="flex items-center justify-between pt-4 pb-2">
            <h5 className="font-semibold">Beneficiaries</h5>
            <div className="text-sm text-gray-400">
              Upto 5 active beneficiaries allowed{" "}
            </div>
          </div>
          <div className="flex flex-col mb-6 ">
            <div className="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
              <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                <div className="overflow-hidden border-b border-gray-200 rounded-md shadow-md">
                  <table className="min-w-full overflow-x-scroll divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th
                          scope="col"
                          className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase"
                        >
                          Name
                        </th>
                        <th
                          scope="col"
                          className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase"
                        >
                          Balance
                        </th>
                        <th
                          scope="col"
                          className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase"
                        ></th>
                        <th scope="col" className="relative px-6 py-3">
                          <span className="sr-only">Edit</span>
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      <BeneficiariesTable
                        beneficiaries={beneficiaries}
                        forceFetchCtr={forceFetchCtr}
                        setForceFetchCtr={setForceFetchCtr}
                      />
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          <ModalAddBeneficiary
            allowedTopups={allowedTopups}
            beneficiaries={beneficiaries}
            forceFetchCtr={forceFetchCtr}
            setForceFetchCtr={setForceFetchCtr}
          />
        </div>
      </div>
    </>
  );
}
