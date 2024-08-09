export default function Component() {
  return (
    <footer className="flex w-full bg-gray-100 text-xs text-gray-400 p-2">
      <div className="">
        © {new Date().getFullYear()}{" "}
        <a href="https://www.bytebeacon.com" className="">
          ByteBeacon, Inc.
        </a>{" "}
        All rights reserved.
      </div>
    </footer>
  );
}
