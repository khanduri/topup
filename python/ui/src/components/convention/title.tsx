export default function Section(props: any) {
  if (props.type === "sidenav-page") {
    return (
      <div
        {...props}
        className={
          "flex flex-col items-start justify-between pb-6 space-y-4 border-b lg:items-center lg:space-y-0 lg:flex-row " +
          props.className
        }
      >
        <h1 className="w-full text-2xl font-semibold whitespace-nowrap">
          {props.children}
        </h1>
      </div>
    );
  }

  if (props.type === "page") {
    return (
      <h2
        {...props}
        className={
          "m-0 box-border border-solid text-3xl font-semibold sm:text-4xl md:text-5xl " +
          props.className
        }
      >
        {props.children}
      </h2>
    );
  }

  if (props.type === "section") {
    return (
      <h5
        {...props}
        className={
          "m-0 box-border border-solid text-lg font-semibold sm:text-xl md:text-2xl " +
          props.className
        }
      >
        {props.children}
      </h5>
    );
  }

  if (props.type === "strong") {
    return (
      <h5
        {...props}
        className={
          "text-md box-border border-solid font-semibold  " + props.className
        }
      >
        {props.children}
      </h5>
    );
  }

  if (props.type === "cursive") {
    return (
      <p
        {...props}
        className={
          "family-cursive pb-3 text-lg font-bold uppercase tracking-wider  lg:items-center lg:justify-center " +
          props.className
        }
      >
        {props.children}
      </p>
    );
  }

  return (
    <div {...props} className={"" + props.className}>
      {props.children}
    </div>
  );
}
