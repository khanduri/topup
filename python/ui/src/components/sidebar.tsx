import { Link, useNavigate, redirect } from "react-router-dom";
import { deleteToken } from "utils/authentication";
import { useAuth } from "./hooks/useAuth";

function IconDashboard() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
      className="w-6 h-6"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M9 17.25v1.007a3 3 0 01-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0115 18.257V17.25m6-12V15a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 15V5.25m18 0A2.25 2.25 0 0018.75 3H5.25A2.25 2.25 0 003 5.25m18 0V12a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 12V5.25"
      />
    </svg>
  );
}
function IconSettings() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
      className="w-6 h-6"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"
      />
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
      />
    </svg>
  );
}
function IconLogout() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
      className="w-6 h-6"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75"
      />
    </svg>
  );
}

export default function Component({
  isOpen,
  setIsOpen,
}: {
  isOpen: boolean;
  setIsOpen: any;
}) {
  // {/* <!-- Sidebar backdrop --> */}
  // {/* <div className="fixed inset-0 z-10 bg-black bg-opacity-20 lg:hidden"></div> */}

  const sidelink = [
    { title: "Dashboard", url: "/dashboard", icon: IconDashboard },
    { title: "Settings", url: "/settings", icon: IconSettings },
  ];

  // const navigate = useNavigate();
  // function logout(e: any) {
  //   e.preventDefault();
  //   deleteToken();
  //   // navigate("/", { replace: true });
  //   redirect("/");
  // }

  const { logout } = useAuth();
  return (
    <aside
      className={
        "fixed bg-gray-50 inset-y-0 z-10 flex flex-col flex-shrink-0 w-64 max-h-screen overflow-hidden transition-all transform border-r shadow-lg lg:z-auto lg:static lg:shadow-none " +
        (isOpen ? "" : " -translate-x-full lg:translate-x-0 lg:w-20 ")
      }
    >
      {/* <!-- sidebar header --> */}
      <div
        className={
          "flex items-center justify-between flex-shrink-0 p-2 " +
          (isOpen ? "" : " lg:justify-center ")
        }
      >
        <span className="p-2 text-xl font-semibold leading-8 whitespace-nowrap">
          {isOpen ? (
            <span className="">TopUp</span>
          ) : (
            <span className="">TU</span>
          )}
        </span>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="p-2 rounded-md lg:hidden"
        >
          <svg
            className="w-6 h-6 text-gray-600"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      {/* <!-- Sidebar links --> */}
      <nav className="flex-1 overflow-hidden hover:overflow-y-auto">
        <ul className="p-2 overflow-hidden">
          {sidelink.map((item, idx) => (
            <li
              key={idx}
              className=" text-gray-500 rounded hover:bg-gray-200  "
            >
              <Link
                to={item.url}
                className={
                  "flex items-center p-2 space-x-2  " +
                  (isOpen ? "" : " justify-center ")
                }
              >
                <item.icon />
                <span className={isOpen ? "" : " lg:hidden "}>
                  {item.title}
                </span>
              </Link>
            </li>
          ))}
          {/* // <!-- Sidebar Links... --> */}
        </ul>
      </nav>

      {/* // <!-- Sidebar footer --> */}
      <div className="flex-shrink-0 p-2 max-h-14">
        <button
          className="flex items-center justify-center w-full px-4 py-2 space-x-1 font-sm tracking-wider border-t rounded-md focus:outline-none focus:ring"
          // onClick={(e) => logout(e)}
          onClick={logout}
        >
          <IconLogout />
          <span className={isOpen ? "" : " lg:hidden "}>Logout</span>
        </button>
      </div>
    </aside>
  );
}
