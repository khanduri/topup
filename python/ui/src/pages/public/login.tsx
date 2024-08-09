// import { toast } from "react-toastify";

import Title from "components/convention/title";
import { useAuth } from "components/hooks/useAuth";
import Logo from "images/logo";
import { useEffect, useState } from "react";
import { Link, redirect, useNavigate, useSearchParams } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import { useGoogleLogin } from "@react-oauth/google";
import { access } from "fs";
import API from "utils/xhr";
import { saveLoginMeta, saveToken } from "utils/authentication";
import LoadingSVG from "images/loading";

export default function Login() {
  const [email, setEmail] = useState("");

  function sendEmailCode(e: any, email: string) {
    e.preventDefault();

    if (email === null || email === undefined || email === "") {
      // toast.error("Email cannot be empty!", { autoClose: 3000 });
    } else {
      // TODO: record email

      const resolveAfter3Sec = new Promise((resolve, reject) =>
        setTimeout(reject, 3000)
      );
      // toast.promise(
      //   resolveAfter3Sec,
      //   {
      //     pending: "Logging in ... ",
      //     success: "Email not onboarded!",
      //     error: "Email not onboarded!",
      //   },
      //   { autoClose: 3000 },
      // );

      let formData = new FormData() as any;
      formData.append("email", email);
      formData.append("form-name", "login");

      // toast.promise(
      //   fetch("/", {
      //     method: "POST",
      //     headers: { "Content-Type": "application/x-www-form-urlencoded" },
      //     body: new URLSearchParams(formData).toString(),
      //   }).then(() => resolveAfter3Sec),
      //   {
      //     pending: "Logging in ... ",
      //     success: "Email not onboarded!",
      //     error: "Email not onboarded!",
      //   },
      //   { autoClose: 3000 }
      // );
    }
  }

  function onChange(email: string) {
    setEmail(email);
  }

  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);

  const login_google = useGoogleLogin({
    onSuccess: (response) => handleLoginSuccess("google", response),
  });

  const handleLoginSuccess = (service: string, response: any) => {
    const access_token = response.access_token;
    // login(access_token);
    // saveToken(access_token);

    const headers = {
      headers: { Authorization: "Bearer " + access_token },
    };
    const url = "/users/auth/" + service;
    API.post(url, {}, headers).then(
      (response: any) => {
        const success = response.data.meta.success;
        if (success) {
          var jwt_token = response.data.data.token;
          saveToken(jwt_token);
          saveLoginMeta(response.data.data.meta);
          login(jwt_token);
          setLoading(false);
        } else {
          alert(response.data.data.message);
        }
      },
      (error: any) => {
        setLoading(false);
      }
    );
  };

  function demoLogin(e: any) {
    e.preventDefault();

    // saveToken("DEMO_LOGIN");
    console.log(login);
    login("DEMO_LOGIN");

    // var destination = searchParams.get("dest") || "/";
    // // redirect(destination);
    // navigate(destination);
  }

  return (
    <div className="bg-white dark:bg-gray-900">
      <div className="flex h-screen justify-center">
        <div
          className="hidden bg-auto lg:block lg:w-2/3"
          style={{
            backgroundImage: `url(static/images/zig-zag.svg)`,
          }}
        >
          <div className="flex h-full items-center bg-gray-900 bg-opacity-70 px-20 text-gray-100">
            <div>
              <Title type="section" className="mb-8 text-2xl">
                The smart way to <i className="text-action-300">TopUp</i>
              </Title>

              <p className="py-1 text-gray-400">We{"'"}re in early beta!</p>
              <p className="py-1 text-gray-400">
                Your login will only work if your email has been onboarded.
              </p>
              <p className="py-1 text-gray-400">
                <a
                  href="mailto:info@bytebeacon.com?subject=Login access request!"
                  className="text-action-500"
                >
                  Please request early access
                </a>{" "}
                for login to work.
              </p>
            </div>
          </div>
        </div>

        <div className="mx-auto flex w-full max-w-md items-center px-6 lg:w-2/6">
          <div className="flex-1">
            <div className="text-center">
              <div className="flex w-full justify-center text-gray-800">
                <Link to="/" className="">
                  <Logo className="h-32 w-32"></Logo>
                </Link>
              </div>

              <p className="mt-3 text-gray-500 dark:text-gray-300">
                Sign in to access your account
              </p>
            </div>

            <div className="mt-8">
              {/* <form name="login" method="POST" data-netlify="true">
                <label
                  htmlFor="email"
                  className="mb-2 block text-sm text-gray-600 dark:text-gray-200"
                >
                  Email Address
                </label>
                <input
                  type="email"
                  name="email"
                  id="email"
                  onChange={(e) => onChange(e.target.value)}
                  placeholder="example@example.com"
                  className="mt-2 block w-full rounded-md border border-gray-200 bg-white px-4 py-2 text-gray-700 placeholder-gray-400 focus:border-primary-400 focus:outline-none focus:ring focus:ring-primary-400 focus:ring-opacity-40 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-300 dark:placeholder-gray-600 dark:focus:border-primary-400"
                />

                <div className="mt-6">
                  <button
                    className="w-full transform rounded-md bg-gray-900 px-4 py-2 tracking-wide text-white transition-colors duration-200 hover:bg-gray-700 focus:bg-gray-700 focus:outline-none focus:ring focus:ring-gray-300 focus:ring-opacity-50"
                    onClick={(e) => sendEmailCode(e, email)}
                  >
                    Login with Email
                  </button>
                </div>
              </form> */}

              {/* <div className="my-8 text-center">OR</div> */}

              {/* <div className="mt-6">
                <button
                  className="w-full transform rounded-md bg-action-700 px-4 py-2 tracking-wide text-white transition-colors duration-200 hover:bg-action-600 focus:bg-action-600 focus:outline-none focus:ring focus:ring-gray-300 focus:ring-opacity-50"
                  onClick={(e) => demoLogin(e)}
                >
                  Demo Login
                </button>
              </div> */}
              {/* <p className="mt-6 text-center text-sm text-gray-400">
                Don{"'"}t have an account yet?{" "}
                <a
                  href="#"
                  className="text-primary-500 hover:underline focus:underline focus:outline-none"
                >
                  Sign up
                </a>
                .
              </p> */}
              <div className="mt-6 ">
                <button
                  className="bg-red-600 hover:bg-red-500 text-white border py-2 w-full rounded-md mt-5 flex justify-center items-center transition-colors duration-200"
                  onClick={() => login_google()}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    height="1em"
                    viewBox="0 0 488 512"
                  >
                    <path
                      d="M488 261.8C488 403.3 391.1 504 248 504 110.8 504 0 393.2 0 256S110.8 8 248 8c66.8 0 123 24.5 166.3 64.9l-67.5 64.9C258.5 52.6 94.3 116.6 94.3 256c0 86.5 69.1 156.6 153.7 156.6 98.2 0 135-70.4 140.8-106.9H248v-85.3h236.1c2.3 12.7 3.9 24.9 3.9 41.4z"
                      fill="currentColor"
                    />
                  </svg>
                  <span className="ml-4">Login with Google</span>
                  {/* <GoogleLogin
                    onSuccess={(credentialResponse) => {
                      console.log(credentialResponse);
                    }}
                    onError={() => {
                      console.log("Login Failed");
                    }}
                  /> */}
                </button>
              </div>
              {loading ? (
                <div className="w-full flex justify-center p-2 ">
                  <LoadingSVG className="text-center h-10 w-10 text-green-700 " />
                </div>
              ) : (
                ""
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
