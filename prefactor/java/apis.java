import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

@Path("/")
public class Api {

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String test() {
        return "Test";
    }
}

import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;

public class JettyServer {
    public static void main(String[] args) throws Exception {
        ServletContextHandler context = new ServletContextHandler(ServletContextHandler.SESSION);
        context.setContextPath("/");
        int port = 8000;
        Server jettyServer = null;
        while(true) {
            try {
                jettyServer = new Server(port);
                break;
            } catch(Exception e) {
                if (++port > 10000) {
                    throw new RuntimeException("Error during jetty server initialization. No port free found from 8000 to 10000", e);
                }
                continue;
            }
        }
        
        jettyServer.setHandler(context);
        ServletHolder jerseyServlet = context.addServlet(org.glassfish.jersey.servlet.ServletContainer.class, "/*");
        jerseyServlet.setInitOrder(0);
        jerseyServlet.setInitParameter("jersey.config.server.provider.classnames", Api.class.getCanonicalName());
        run(jettyServer);
    }

    private static void run(Server server) throws Exception {
        try {
            server.run();
            server.join();
        } finally {
            server.destroy();
        }
    }
}

