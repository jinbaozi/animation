/*
 * Decompiled with CFR 0.152.
 */
package com.cmbcdba;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Timestamp;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;
import java.util.Random;

public class WorkLoadManager {
    public static String dbtype;
    public static String logfile;
    public static String tpslog;
    public static int loop;
    public static int[] rates;
    public static int buffer;
    public static String URL;
    public static String userName;
    public static String password;
    public static int numberCount;
    public static String tableName;
    public static String tablespace;
    public static int totalTrans;
    public static int tablenum;
    public static String sql;
    public static SimpleDateFormat df;

    public WorkLoadManager() {
    }

    public WorkLoadManager(String logfile, int loop, int[] rates, int buffer, String URL2, String userName, String password) {
        WorkLoadManager.logfile = logfile;
        WorkLoadManager.loop = loop;
        WorkLoadManager.rates = rates;
        WorkLoadManager.buffer = buffer;
        URL = URL2;
        WorkLoadManager.userName = userName;
        WorkLoadManager.password = password;
    }

    public static synchronized void appendMethod(String fileName, String content) {
        try {
            FileWriter writer = new FileWriter(fileName, true);
            writer.write(content + "\r\n");
            writer.close();
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static String formatDouble(double d) {
        DecimalFormat format = (DecimalFormat)NumberFormat.getInstance();
        format.applyPattern("0.0");
        return format.format(d);
    }

    public static void main(String[] args) throws Exception {
        String configfile = "";
        if (args.length == 0) {
            System.out.print("Pls input config file location: ");
            InputStreamReader stdin = new InputStreamReader(System.in);
            BufferedReader bufin = new BufferedReader(stdin);
            configfile = bufin.readLine();
        }
        System.out.println("Start");
        Properties prop = new Properties();
        if (configfile == "") {
            configfile = args[0];
        }
        FileInputStream in = new FileInputStream(configfile);
        prop.load(in);
        dbtype = prop.getProperty("dbtype");
        logfile = prop.getProperty("log");
        tpslog = prop.getProperty("tpslog");
        int threadcount = new Integer(prop.getProperty("thread"));
        loop = new Integer(prop.getProperty("loop"));
        String ratesStr = prop.getProperty("rate");
        buffer = new Integer(prop.getProperty("buffer"));
        URL = prop.getProperty("url");
        userName = prop.getProperty("username");
        password = prop.getProperty("password");
        tableName = prop.getProperty("tablename");
        tablespace = prop.getProperty("tablespace");
        tablenum = new Integer(prop.getProperty("tablenum"));
        sql = prop.getProperty("sql");
        String[] ratesGrp = ratesStr.split(",");
        rates = new int[4];
        WorkLoadManager.rates[0] = new Integer(ratesGrp[0]);
        WorkLoadManager.rates[1] = new Integer(ratesGrp[1]);
        WorkLoadManager.rates[2] = new Integer(ratesGrp[2]);
        WorkLoadManager.rates[3] = new Integer(ratesGrp[3]);
        if (!"".equals(logfile)) {
            WorkLoadManager.appendMethod(logfile, "----------------------------------------------------------------");
            WorkLoadManager.appendMethod(logfile, "insert(us)\tupdate(us)\tdelete(us)\tquery(us)");
        }
        for (int i = 1; i <= tablenum; ++i) {
            KeySequence ks = new KeySequence();
            ks.init(i);
            TimeMonitor tm = new TimeMonitor();
            for (int j = 0; j < threadcount / tablenum; ++j) {
                new loadRunner(ks, tm, loop, i).start();
                Thread.sleep(100L);
            }
        }
        Thread.sleep(1000L);
        while (numberCount != 0) {
            try {
                int totalTrans_pre = totalTrans;
                Thread.sleep(1000L);
                int tps = totalTrans - totalTrans_pre;
                WorkLoadManager.appendMethod(tpslog, df.format(new Date()) + "\t" + new Integer(tps).toString());
            }
            catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        System.out.println("End");
    }

    static {
        numberCount = 0;
        df = new SimpleDateFormat("HH:mm:ss");
    }

    public static class loadRunner
    extends Thread {
        private Connection conn = null;
        private PreparedStatement stmt_inst = null;
        private PreparedStatement stmt_updt = null;
        private PreparedStatement stmt_del = null;
        private PreparedStatement stmt_sel = null;
        private KeySequence ks;
        private TimeMonitor tm;
        private int loop;
        private int suffix;

        public loadRunner(KeySequence ks, TimeMonitor tm, int loop, int suffix) {
            this.ks = ks;
            this.tm = tm;
            this.loop = loop;
            this.suffix = suffix;
        }

        /*
         * WARNING - Removed try catching itself - possible behaviour change.
         */
        @Override
        public void run() {
            try {
                ++numberCount;
                try {
                    System.out.println("Run");
                    this.conn = DriverManager.getConnection(URL, userName, password);
                }
                catch (Exception e) {
                    e.printStackTrace();
                }
                this.conn.setAutoCommit(true);
                this.stmt_inst = this.conn.prepareStatement("insert into " + tableName + "_" + this.suffix + "(c1,c2,c3,c4,c5) values (?,?,?,?,?)");
                this.stmt_updt = this.conn.prepareStatement("update " + tableName + "_" + this.suffix + " set c3=? where c1=?");
                this.stmt_del = this.conn.prepareStatement("delete from " + tableName + "_" + this.suffix + " where c1=?");
                this.stmt_sel = "".equals(sql) || sql == null ? this.conn.prepareStatement("select * from " + tableName + "_" + this.suffix + " where c1 =?") : this.conn.prepareStatement(sql);
                long totalInstTime = 0L;
                long totalUptTime = 0L;
                long totalDelTime = 0L;
                long totalQueryTime = 0L;
                int startkey = 0;
                int endkey = 0;
                StringBuilder context = new StringBuilder();
                for (int i = 0; i < this.loop || this.loop == 0; ++i) {
                    long istart = 0L;
                    long iend = 0L;
                    long ustart = 0L;
                    long uend = 0L;
                    long dstart = 0L;
                    long dend = 0L;
                    long sstart = 0L;
                    long send = 0L;
                    long instTime = 0L;
                    long uptTime = 0L;
                    long delTime = 0L;
                    long queryTime = 0L;
                    int j0 = rates[0];
                    int j1 = rates[1];
                    int j2 = rates[2];
                    int j3 = rates[3];
                    while (j0 > 0 || j1 > 0 || j2 > 0 || j3 > 0) {
                        if (j0 > 0) {
                            if (startkey == endkey) {
                                endkey = this.ks.nextBufKey();
                                startkey = endkey - buffer;
                            }
                            this.stmt_inst.setInt(1, startkey);
                            this.stmt_inst.setInt(2, startkey);
                            this.stmt_inst.setString(3, "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" + startkey);
                            this.stmt_inst.setString(4, "ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc" + startkey);
                            this.stmt_inst.setTimestamp(5, new Timestamp(this.tm.getCurrentTime()));
                            istart = this.tm.getCurrentTimeNano();
                            this.stmt_inst.executeUpdate();
                            ++totalTrans;
                            iend = this.tm.getCurrentTimeNano();
                            instTime = (iend - istart) / 1000L;
                            totalInstTime += instTime;
                            ++startkey;
                            --j0;
                        }
                        if (j1 > 0) {
                            int ukey = this.ks.getKey();
                            this.stmt_updt.setString(1, "modifiedasdfsdfvsdfsdfsdfwefsdfsdfsdfsdfcvfghjhjggvcsdfsdfdfgdg" + ukey);
                            this.stmt_updt.setInt(2, ukey);
                            ustart = this.tm.getCurrentTimeNano();
                            this.stmt_updt.executeUpdate();
                            ++totalTrans;
                            uend = this.tm.getCurrentTimeNano();
                            uptTime = (uend - ustart) / 1000L;
                            totalUptTime += uptTime;
                            --j1;
                        }
                        if (j2 > 0) {
                            int dkey = this.ks.getKey();
                            this.stmt_del.setInt(1, dkey);
                            dstart = this.tm.getCurrentTimeNano();
                            this.stmt_del.executeUpdate();
                            ++totalTrans;
                            dend = this.tm.getCurrentTimeNano();
                            delTime = (dend - dstart) / 1000L;
                            totalDelTime += delTime;
                            --j2;
                        }
                        if (j3 > 0) {
                            if ("".equals(sql) || sql == null) {
                                int skey = this.ks.getKey();
                                this.stmt_sel.setInt(1, skey);
                            }
                            sstart = this.tm.getCurrentTimeNano();
                            this.stmt_sel.executeQuery();
                            ++totalTrans;
                            send = this.tm.getCurrentTimeNano();
                            queryTime = (send - sstart) / 1000L;
                            totalQueryTime += queryTime;
                            --j3;
                        }
                        context.append(instTime);
                        context.append("\t");
                        context.append(uptTime);
                        context.append("\t");
                        context.append(delTime);
                        context.append("\t");
                        context.append(queryTime);
                        context.append("\t");
                        instTime = -1L;
                        uptTime = -1L;
                        delTime = -1L;
                        queryTime = -1L;
                    }
                    if (i % buffer != 0 && i != this.loop - 1) continue;
                    if (!"".equals(logfile)) {
                        WorkLoadManager.appendMethod(logfile, context.toString().substring(0, context.length() - 1));
                    }
                    context.delete(0, context.length());
                }
                this.tm.calTotalInstTime(totalInstTime);
                this.tm.calTotalUptTime(totalUptTime);
                this.tm.calTotalDelTime(totalDelTime);
                this.tm.calTotalQueryTime(totalQueryTime);
            }
            catch (Exception e) {
                e.printStackTrace();
                try {
                    loadRunner.sleep(10000L);
                }
                catch (InterruptedException interruptedException) {
                    // empty catch block
                }
                this.run();
            }
            finally {
                try {
                    this.stmt_updt.close();
                    this.stmt_inst.close();
                    this.stmt_del.close();
                    this.stmt_sel.close();
                    this.conn.close();
                    --numberCount;
                }
                catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public static class TimeMonitor {
        private long totalInstTime;
        private long totalUptTime;
        private long totalDelTime;
        private long totalQueryTime;

        public long getTotalInstTime() {
            return this.totalInstTime;
        }

        public long getTotalUptTime() {
            return this.totalUptTime;
        }

        public long getTotalDelTime() {
            return this.totalDelTime;
        }

        public long getTotalQueryTime() {
            return this.totalQueryTime;
        }

        public long getCurrentTime() {
            return System.currentTimeMillis();
        }

        public long getCurrentTimeNano() {
            return System.nanoTime();
        }

        public synchronized void calTotalInstTime(long time) {
            this.totalInstTime += time;
        }

        public synchronized void calTotalUptTime(long time) {
            this.totalUptTime += time;
        }

        public synchronized void calTotalDelTime(long time) {
            this.totalDelTime += time;
        }

        public synchronized void calTotalQueryTime(long time) {
            this.totalQueryTime += time;
        }
    }

    public static class KeySequence {
        private int key = 0;
        private int currentKey = 0;

        public void init(int suffix) {
            try {
                if (dbtype.equalsIgnoreCase("DB2")) {
                    Class.forName("com.ibm.db2.jcc.DB2Driver");
                } else if (dbtype.equalsIgnoreCase("Oracle")) {
                    Class.forName("oracle.jdbc.driver.OracleDriver");
                } else if (dbtype.equalsIgnoreCase("MySQL")) {
                    Class.forName("com.mysql.jdbc.Driver");
                } else if (dbtype.equalsIgnoreCase("openGauss")) {
                    Class.forName("org.postgresql.Driver");
                }
                Connection conn = DriverManager.getConnection(URL, userName, password);
                System.out.println("init");
                Statement stmt = conn.createStatement();
                try {
                    if (dbtype.equalsIgnoreCase("DB2")) {
                        stmt.execute("create table " + tableName + "_" + suffix + " (c1 int, c2 bigint, c3 varchar(100),c4 char(100), c5 timestamp) in " + tablespace);
                        stmt.execute("create index idx_1_" + tableName + "_" + suffix + " on " + tableName + "_" + suffix + " (c1)");
                        stmt.execute("create index idx_2_" + tableName + "_" + suffix + " on " + tableName + "_" + suffix + " (c1,c2,c3)");
                    } else if (dbtype.equalsIgnoreCase("Oracle")) {
                        stmt.execute("create table " + tableName + "_" + suffix + " (c1 int, c2 number, c3 varchar2(100),c4 char(100), c5 timestamp) tablespace " + tablespace);
                        stmt.execute("create index idx_1_" + tableName + "_" + suffix + " on " + tableName + "_" + suffix + " (c1)");
                        stmt.execute("create index idx_2_" + tableName + "_" + suffix + " on " + tableName + "_" + suffix + " (c1,c2,c3)");
                    } else if (dbtype.equalsIgnoreCase("MySQL")) {
                        stmt.execute("create table " + tableName + "_" + suffix + " (c1 int, c2 int, c3 varchar(100),c4 char(100), c5 datetime(6))");
                        stmt.execute("alter table " + tableName + " add primary key (c1)");
                        stmt.execute("create index idx_2_" + tableName + "_" + suffix + " on " + tableName + "_" + suffix + " (c1,c2,c3)");
                    } else if (dbtype.equalsIgnoreCase("openGauss")) {
                        stmt.execute("create table " + tableName + "_" + suffix + " (c1 int, c2 int, c3 varchar(100),c4 char(100), c5 date)");
                        stmt.execute("create index idx_1_" + tableName + "_" + suffix + " on " + tableName + "_" + suffix + " (c1)");
                        stmt.execute("create index idx_2_" + tableName + "_" + suffix + " on " + tableName + "_" + suffix + " (c1,c2,c3)");
                    }
                }
                catch (Exception exception) {
                    // empty catch block
                }
                ResultSet rs = stmt.executeQuery("select count(*) from " + tableName + "_" + suffix);
                rs.next();
                this.currentKey = this.key = rs.getInt(1);
                System.out.println(this.key);
                rs.close();
                stmt.close();
                conn.close();
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }

        public synchronized int nextKey() {
            ++this.key;
            return this.key;
        }

        public synchronized int nextBufKey() {
            this.key += buffer;
            return this.key;
        }

        public int currentKey() {
            return this.currentKey;
        }

        public int getKey() {
            Random r = new Random();
            return r.nextInt(this.currentKey + 1);
        }
    }
}
