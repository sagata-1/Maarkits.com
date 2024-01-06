import React from "react";
import { Tabs, Tab } from "react-bootstrap";
export default function HistoryOrder() {
  return (
    <>
      <div className="market-history-tab market-order mt15">
        <Tabs defaultActiveKey="portfolio">
          <Tab eventKey="portfolio" title="Portfolio">
            <div className="market-carousel-item" style={{ margin: "10px" }}>
              <div className="row">
                <div className="col-sm-2">
                  <h2>$13110.0</h2>
                  <p>Current Value</p>
                </div>

                <div className="col-sm-2">
                  <h2>$3110.0</h2>
                  <p>Profit/Loss</p>
                </div>
                <div className="col-sm-3">
                  <h2>$1100.0</h2>
                  <p>Starting Amount</p>
                </div>

                <div className="col-sm-3">
                  <h2>$9999.0</h2>
                  <p>Total Amount Invested</p>
                </div>
                <div className="col-sm-2">
                  <h2>$1001.0</h2>
                  <p>Avaialable Amount</p>
                </div>
              </div>
            </div>

            <div className="table-responsive-1">
              <table className="table star-active1">
                <thead>
                  <tr>
                    <th>PRODUCT</th>
                    <th>MKT PRICE</th>
                    <th>INVESTED</th>
                    <th>RETURNS</th>
                    <th>CURRENT </th>
                  </tr>
                </thead>
                <tbody>
                  <tr data-href="exchange-light.html">
                    <td>
                      AA
                      <div className="w10" style={{ width: "200px" }}>
                        <span>2222 shares </span>
                        <span style={{ marginBottom: "4px" }}></span>
                        <span>Avg. $4.50</span>
                      </div>
                    </td>
                    <td className="">$5.90</td>
                    <td>$9999.0</td>
                    <td className="green">+$3110.80</td>
                    <td className="green">+$13110.0</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </Tab>
          <Tab eventKey="open-orders" title="Open Orders">
            <ul className="d-flex justify-content-between market-order-item">
              <li>Time</li>
              <li>All pairs</li>
              <li>All Types</li>
              <li>Buy/Sell</li>
              <li>Price</li>
              <li>Amount</li>
              <li>Executed</li>
              <li>Unexecuted</li>
            </ul>
            <span className="no-data">
              <i className="icon ion-md-document"></i>
              No data
            </span>
          </Tab>
          <Tab eventKey="closed-orders" title="Closed Orders">
            <ul className="d-flex justify-content-between market-order-item">
              <li>Time</li>
              <li>All pairs</li>
              <li>All Types</li>
              <li>Buy/Sell</li>
              <li>Price</li>
              <li>Amount</li>
              <li>Executed</li>
              <li>Unexecuted</li>
            </ul>
            <span className="no-data">
              <i className="icon ion-md-document"></i>
              No data
            </span>
          </Tab>
          <Tab eventKey="order-history" title="Order history">
            <ul className="d-flex justify-content-between market-order-item">
              <li>Time</li>
              <li>All pairs</li>
              <li>All Types</li>
              <li>Buy/Sell</li>
              <li>Price</li>
              <li>Amount</li>
              <li>Executed</li>
              <li>Unexecuted</li>
            </ul>
            <span className="no-data">
              <i className="icon ion-md-document"></i>
              No data
            </span>
          </Tab>
          <Tab eventKey="balance" title="Balance">
            <ul className="d-flex justify-content-between market-order-item">
              <li>Time</li>
              <li>All pairs</li>
              <li>All Types</li>
              <li>Buy/Sell</li>
              <li>Price</li>
              <li>Amount</li>
              <li>Executed</li>
              <li>Unexecuted</li>
            </ul>
            <span className="no-data">
              <i className="icon ion-md-document"></i>
              No data
            </span>
          </Tab>
        </Tabs>
      </div>
    </>
  );
}