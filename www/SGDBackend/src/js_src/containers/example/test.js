import assert from 'assert';
import React from 'react';
import { renderToString } from 'react-dom/server';

import Help from './index';

describe('Help', () => {
  it('should be able to render to an HTML string', () => {
    let htmlString = renderToString(<Help />);
    assert.equal(typeof htmlString, 'string');
  });
});
