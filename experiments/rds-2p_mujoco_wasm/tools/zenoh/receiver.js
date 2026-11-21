import { Config, Session } from "@eclipse-zenoh/zenoh-ts";

const key = "rds2p/sim/motors/commands";
const protocol = location.protocol === "https:" ? "wss" : "ws";
const session = await Session.open(new Config(`${protocol}/${location.hostname}:10000`));
await session.declareSubscriber(key, {
  handler(sample) {
    try {
      const message = JSON.parse(sample.payload().toString());
      console.log("[RDS2P] MotorCommands", JSON.stringify(message));
    } catch (error) {
      console.error("[RDS2P] Invalid command payload", error);
    }
  }
});
console.info("[RDS2P] Listening on", key);
